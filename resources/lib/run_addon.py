# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# noinspection PyUnresolvedReferences
from codequick import Route, Resolver, Script, Listitem
from codequick import run as codequick_run
from codequick.utils import bold, color
from codequick.script import Settings
from .exceptions import NotificationError
from .platforms.nhl66 import NHL66, Game, GameStatus, Link, PremiumLinkGenerator, Auth, LinkStatus
from .platforms.nhl66.consts import PREMIUM_ORIGIN
from typing import List
from .gui.premium.login import LoginWindow
from .gui.premium.account import AccountWindow
from .gui.proxies.proxies import ProxiesWindow
from .gui.modal import doModal
import xbmcgui, xbmcaddon, xbmc, urllib.parse, inputstreamhelper, pyxbmct


# Labels Constants
LIVE_EVENTS_LABEL = 30000
REPLAY_LABEL = 30004

# View mode
VIEW_MODE = None


def run():
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
    live_events_label = color(bold(plugin.localize(LIVE_EVENTS_LABEL)), 'limegreen')
    live_events_item = Listitem.from_dict(get_games, live_events_label, params={'status_filter': [GameStatus.LIVE, GameStatus.PREGAME]})
    live_events_item.info.title = live_events_label
    yield live_events_item

    # Game Replays
    replay_label = color(bold(plugin.localize(REPLAY_LABEL)), 'gold')
    replay_item = Listitem.from_dict(get_games, replay_label, params={'status_filter': [GameStatus.FINAL]})
    replay_item.info.title = replay_label
    yield replay_item

    # Premium
    premium_label = f'{color(bold("Premium Account"), "magenta")}'
    premium_item = Listitem.from_dict(premium_root, premium_label)
    premium_item.info.title = premium_label
    yield premium_item

    # Premium
    proxies_label = f'{color(bold("Proxies"), "cyan")}'
    proxies_item = Listitem.from_dict(proxies_modal, proxies_label)
    proxies_item.info.title = proxies_label
    yield proxies_item


@Route.register
def premium_root(plugin: Route):
    window = None
    if Auth.is_premium():
        window = AccountWindow()
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
    pregame_events = []
    final_events = []

    for game in schedule:
        try:
            # Create the list item
            listitem = Listitem.from_dict(game_links, game.label, params={'game_id': game.id})
            listitem.info.title = game.label
            if game.thumbnail:
                listitem.art.thumb  = game.thumbnail
                listitem.art.fanart = game.thumbnail
                listitem.art.poster = game.thumbnail

            # Add it in the right category
            if game.status == GameStatus.PREGAME:
                pregame_events.append(listitem)
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
        elif status == GameStatus.PREGAME:
            events.extend(pregame_events)
        elif status == GameStatus.FINAL:
            events.extend(final_events)

    return events



@Route.register(content_type='videos')
def game_links(plugin, game_id):
    """
    The links list page route.
    """

    global VIEW_MODE
    VIEW_MODE = '53' # Shift

    # Retrieve game
    game: Game = Game.from_id(game_id, skip_cache=True)
    if game is None:
        raise NotificationError('Game Not Found', 'Cannot find the game details.')
    
    # Retrieve links
    links = game.get_links(skip_cache=False)

    # Create listitems
    for link in links:
        try:
            # Standard link
            std_listitem = Listitem.from_dict(play_link, link.label, params={'link_id': link.id, 'premium': False})
            std_listitem.info.title = link.label
            if link.thumbnail:
                std_listitem.art.thumb  = link.thumbnail
                std_listitem.art.fanart = link.thumbnail
                std_listitem.art.poster = link.thumbnail
            yield std_listitem
            if link.premium_flavor:
                std_listitem = Listitem.from_dict(play_link, link.premium_label, params={'link_id': link.id, 'premium': True})
                std_listitem.info.title = link.premium_label
                if link.thumbnail:
                    std_listitem.art.thumb  = link.thumbnail
                    std_listitem.art.fanart = link.thumbnail
                    std_listitem.art.poster = link.thumbnail
                yield std_listitem
        except Exception as e:
            Script.log(str(e), lvl=Script.ERROR)



@Resolver.register
def play_link(plugin: Resolver, link_id, premium):
    """
    The link playing route.
    """

    # Retrieve the link
    link: Link = Link.from_id(link_id, skip_cache=True)
    if link is None:
        raise NotificationError('Link Not Found', 'Cannot find the requested link.')
    
    # Retrieve the url
    url = PremiumLinkGenerator.generate_premium_link(link) if premium else link.url
    if url is None:
        raise NotificationError('Unavailable', 'This link is not available yet.')

    # Build the listitem
    helper = inputstreamhelper.Helper('hls')
    if helper.check_inputstream():
        listitem = Listitem()
        listitem.label = link.label
        listitem.set_path(url)
        listitem.listitem.setContentLookup(False)
        listitem.listitem.setMimeType('application/x-mpegURL')
        listitem.listitem.setProperty('inputstream', helper.inputstream_addon)
        listitem.listitem.setProperty('inputstream.adaptive.manifest_type', 'hls')
        listitem.listitem.setProperty('inputstream.adaptive.stream_selection_type', 'ask-quality')

        # Set premium-specific requests headers
        if premium:
            headers = {
                'User-Agent': str(Settings.get_string('user_agent')),
                'Origin': PREMIUM_ORIGIN
            }
            listitem.listitem.setProperty('inputstream.adaptive.manifest_headers', urllib.parse.urlencode(headers))
            listitem.listitem.setProperty('inputstream.adaptive.stream_headers', urllib.parse.urlencode(headers))

        # Force live
        if link.status in [LinkStatus.LIVE, LinkStatus.PLANNED, LinkStatus.DELAYED]:
            listitem.listitem.setProperty('ResumeTime', '43200')
            listitem.listitem.setProperty('TotalTime', '1')

        # Force replay
        if link.status in [LinkStatus.REPLAY]:
            listitem.listitem.setProperty('ResumeTime', '1')
            listitem.listitem.setProperty('TotalTime', '1')

    return listitem