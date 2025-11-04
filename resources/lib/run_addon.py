# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# noinspection PyUnresolvedReferences
from codequick import Route, Resolver, Script, Listitem
from codequick import run as codequick_run
from codequick.utils import bold, color
from codequick.script import Settings
from .common.labels import labels
from .common.utils import get_kodi_version
from .exceptions import NotificationError
from .platforms.nhl66 import NHL66, Game, GameStatus, Auth, MediaEvent, StreamInfo, MediaEventStatus
from .platforms.nhl66.consts import PREMIUM_ORIGIN
from typing import List
from .gui.premium.login import LoginWindow
from .gui.premium.account import AccountWindow
from .gui.premium.expired import ExpiredWindow
from .gui.proxies.proxies import ProxiesWindow
from .gui.modal import doModal
import xbmcgui, xbmcaddon, xbmc, urllib.parse, inputstreamhelper, pyxbmct

# View mode
VIEW_MODE = None


def run():
    Script.log(f'Kodi version is {str(get_kodi_version())}')
    addon_data = xbmcaddon.Addon()
    addon_icon = addon_data.getAddonInfo('icon')
    try:
        try:
            codequick_run(process_errors=False)
            if VIEW_MODE != None:
                xbmc.executebuiltin("Container.SetViewMode({})".format(VIEW_MODE))
        except RuntimeError as e:
            if e.args[0] == 'No items found.':
                return
            raise
    except NotificationError as e:
        Script.logger.exception(f'{str(e.title)}: {str(e.message)}')
        dialog = xbmcgui.Dialog()
        dialog.notification(e.title, e.message, addon_icon)
        if e.args[0] == 'No items found.':
            return
    except Exception as e:
        Script.logger.exception(str(e))
        dialog = xbmcgui.Dialog()
        dialog.notification(e.__class__.__name__, str(e), addon_icon)
        return




@Route.register(content_type='videos', update_listing=True)
def root(plugin: Route):
    """
    The home page route.
    """
    # Live Events
    live_events_label = color(bold(plugin.localize(labels.get('live_events'))), 'limegreen')
    live_events_item = Listitem.from_dict(get_games, live_events_label, params={'status_filter': [GameStatus.LIVE, GameStatus.PLANNED]})
    live_events_item.info.title = live_events_label
    yield live_events_item

    # Game Replays
    replay_label = color(bold(plugin.localize(labels.get('game_replays'))), 'gold')
    replay_item = Listitem.from_dict(get_games, replay_label, params={'status_filter': [GameStatus.FINAL]})
    replay_item.info.title = replay_label
    yield replay_item

    # Premium
    premium_label = f'{color(bold(plugin.localize(labels.get("premium_account"))), "magenta")}'
    premium_item = Listitem.from_dict(premium_root, premium_label)
    premium_item.info.title = premium_label
    yield premium_item

    # Premium
    proxies_label = f'{color(bold(plugin.localize(labels.get("proxies"))), "cyan")}'
    proxies_item = Listitem.from_dict(proxies_modal, proxies_label)
    proxies_item.info.title = proxies_label
    yield proxies_item


@Route.register
def premium_root(plugin: Route):
    window = None
    if Auth.is_logged():
        if Auth.is_premium():
            window = AccountWindow()
        else:
            window = ExpiredWindow()
    else:
        window = LoginWindow()
    
    if window:
        window.doModal()
        del window
    return False

@Route.register
def proxies_modal(plugin: Route):
    doModal(ProxiesWindow)
    return False


@Route.register(content_type='videos')
def get_games(plugin: Route, status_filter: List[GameStatus]):
    """
    The games list page route.
    """

    global VIEW_MODE
    VIEW_MODE = '53' # Shift

    schedule = NHL66.get_schedule()

    live_events = []
    planned_events = []
    final_events = []

    for game in schedule:
        try:
            # Create the list item
            listitem = Listitem.from_dict(game_media_events, game.label, params={'game_id': game.id})
            listitem.info.title = game.label
            if game.thumbnail:
                listitem.art.thumb  = game.thumbnail
                listitem.art.poster = game.poster
                listitem.art.icon   = game.square

            # Add it in the right category
            if game.status == GameStatus.PLANNED:
                planned_events.append(listitem)
            elif game.status == GameStatus.LIVE:
                live_events.append(listitem)
            elif game.status == GameStatus.FINAL:
                final_events.append(listitem)
        except Exception as e:
            Script.log(str(e), lvl=Script.ERROR)

    events = []
    for status in status_filter:
        if status == GameStatus.LIVE:
            events.extend(live_events)
        elif status == GameStatus.PLANNED:
            events.extend(planned_events)
        elif status == GameStatus.FINAL:
            events.extend(final_events)

    return events



@Route.register(content_type='videos')
def game_media_events(plugin, game_id):
    """
    The media events list page route.
    """

    global VIEW_MODE
    VIEW_MODE = '53' # Shift

    # Retrieve game
    game: Game = Game.from_id(game_id, skip_cache=True)
    if game is None:
        raise NotificationError('Game Not Found', 'Cannot find the game details.')
    
    # Retrieve media events
    media_events = game.get_media_events(skip_cache=True)
    print(media_events)

    # Create listitems
    for media_event in media_events:
        try:
            # Standard link
            std_listitem = Listitem.from_dict(play_media_event, media_event.label, params={'media_event_id': media_event.id, 'premium': False})
            std_listitem.info.title = media_event.label
            if media_event.thumbnail:
                std_listitem.art.thumb  = media_event.thumbnail
                std_listitem.art.fanart = media_event.thumbnail
                std_listitem.art.poster = media_event.thumbnail
            yield std_listitem
            # if link.premium_flavor:
            #     std_listitem = Listitem.from_dict(play_link, link.premium_label, params={'link_id': link.id, 'premium': True})
            #     std_listitem.info.title = link.premium_label
            #     if link.thumbnail:
            #         std_listitem.art.thumb  = link.thumbnail
            #         std_listitem.art.fanart = link.thumbnail
            #         std_listitem.art.poster = link.thumbnail
            #     yield std_listitem
        except Exception as e:
            Script.log(str(e), lvl=Script.ERROR)



@Resolver.register
def play_media_event(plugin: Resolver, media_event_id, premium):
    """
    The media event playing route.
    """

    # Retrieve the media event
    media_event: MediaEvent = MediaEvent.from_id(media_event_id, skip_cache=False)
    if media_event is None:
        raise NotificationError('Media Event Not Found', 'Cannot find the requested media event.')
    
    # Retrieve the stream info
    stream_info: StreamInfo = media_event.get_stream_info(premium)
    if stream_info is None:
        raise NotificationError('Stream Info Not Found', 'Cannot find the requested stream info.')

    # Build the listitem
    helper = inputstreamhelper.Helper('hls')
    if helper.check_inputstream():
        listitem = Listitem()
        listitem.label = media_event.label
        listitem.set_path(stream_info.url)
        listitem.listitem.setContentLookup(False)
        listitem.listitem.setMimeType('application/x-mpegURL')
        listitem.listitem.setProperty('inputstream', helper.inputstream_addon)
        listitem.listitem.setProperty('inputstream.adaptive.manifest_type', 'hls')
        listitem.listitem.setProperty('inputstream.adaptive.stream_selection_type', 'ask-quality')

        # # Set premium-specific requests headers
        # if premium:
        #     headers = {
        #         'User-Agent': str(Settings.get_string('user_agent')),
        #         'Origin': PREMIUM_ORIGIN
        #     }
        #     listitem.listitem.setProperty('inputstream.adaptive.manifest_headers', urllib.parse.urlencode(headers))
        #     listitem.listitem.setProperty('inputstream.adaptive.stream_headers', urllib.parse.urlencode(headers))

        # Legacy resume time fix
        if Settings.get_boolean('legacy_resume_fix'):
            Script.log('Applying legacy resume time fix.')
            # Force live
            if media_event.status in [MediaEventStatus.LIVE, MediaEventStatus.PLANNED, MediaEventStatus.DELAYED]:
                if get_kodi_version() >= 20.0:
                    listitem.listitem.getVideoInfoTag().setResumePoint(60*60*24*40, 1)
                else:
                    listitem.listitem.setProperty('ResumeTime', str(60*60*24*40))
                    listitem.listitem.setProperty('TotalTime', '1')
            # Force replay
            if media_event.status in [MediaEventStatus.REPLAY]:
                if get_kodi_version() >= 20.0:
                    listitem.listitem.getVideoInfoTag().setResumePoint(1, 1)
                else:
                    listitem.listitem.setProperty('ResumeTime', '1')
                    listitem.listitem.setProperty('TotalTime', '1')

    return listitem