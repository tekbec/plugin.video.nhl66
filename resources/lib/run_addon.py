# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# noinspection PyUnresolvedReferences
from codequick import Route, Resolver, Script, Listitem
from codequick import run as codequick_run
from codequick.utils import bold, color, italic
import json
from datetime import datetime
from .common.url import encode_proxy_url
from .common.requests import get
from .common.thumbnails import get_thumbnail_url
from .platforms.thesportsdb.schedule import get_game
from .platforms.thesportsdb.tvevents import get_tv_events
from .exceptions import NotificationError
import xbmcgui, xbmcaddon, xbmc

# API Constants
NHL66_API_BASE_URL = 'https://api.nhl66.ir'
NHL66_SCHEDULE_PATH = '/api/sport/stateshot'

# Thumbnails
NHLTV_THUMB     = 'https://i.imgur.com/HGsNesm.png'
ESPN_THUMB      = 'https://i.imgur.com/09KBp1W.png'
TVASPORTS_THUMB = 'https://i.imgur.com/lonf7w3.png'
RDS_THUMB       = 'https://i.imgur.com/qhrFsYh.png'
SPORTSNET_THUMB = 'https://i.imgur.com/qB7bKBT.png'

# Labels Constants
LIVE_EVENTS_LABEL = 30000
LIVE_LABEL = 30001
PREGAME_LABEL = 30002
FINAL_LABEL = 30003
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




@Route.register(content_type='files')
def root(plugin: Route):
    """
    :param Route plugin: The plugin parent object.
    """
    live_events_label = color(bold(plugin.localize(LIVE_EVENTS_LABEL)), 'limegreen')
    live_events_item = Listitem.from_dict(get_games, live_events_label, params={'types': ['live', 'pregame']})
    live_events_item.info.title = live_events_label
    yield live_events_item
    replay_label = color(bold(plugin.localize(REPLAY_LABEL)), 'gold')
    replay_item = Listitem.from_dict(get_games, replay_label, params={'types': ['final']})
    replay_item.info.title = replay_label
    yield replay_item


@Route.register(content_type='videos')
def get_games(plugin: Route, types: list):

    global VIEW_MODE
    VIEW_MODE = '53' # Shift

    # Make the request
    plugin.log('Getting NHL66 schedule...', lvl = Script.DEBUG)
    response = get(NHL66_API_BASE_URL + NHL66_SCHEDULE_PATH, 'nhl66')
    response.raise_for_status()

    # Parse the response
    state = json.loads(response.text)
    games = state['games']
    plugin.log(f'Found {str(len(games))} games.', lvl = Script.DEBUG)

    # Parse each game
    live_events = []
    pregame_events = []
    final_events = []
    plugin.log(f'Parsing games...', lvl = Script.DEBUG)
    for game in games:
        try:
            start_datetime = datetime.fromisoformat(game['start_datetime'].replace('Z','+00:00'))

            # Get thumbnail URL
            thumbnail = get_thumbnail_url(game['home_abr'], game['away_abr'])
            
            # Build the label
            label = f'{game["away_name"]} @ {game["home_name"]} - {italic(start_datetime.astimezone().strftime("%Y/%m/%d - %H:%M"))}'
            if game['status'] == 'P':
                label = f'{color(bold(plugin.localize(PREGAME_LABEL)), "deeppink")} - {label}'
            elif game['status'] == 'I':
                label = f'{color(bold(plugin.localize(LIVE_LABEL)), "limegreen")} - {label}'
            elif game['status'] == 'F':
                label = f'{color(bold(plugin.localize(FINAL_LABEL)), "gold")} - {label}'

            # Create the list item
            listitem = Listitem.from_dict(game_links, label, params={'game_id': game['id']})
            listitem.info.title = label
            if thumbnail:
                listitem.art.thumb  = thumbnail
                listitem.art.fanart = thumbnail
                listitem.art.poster = thumbnail

            # Add it in the right category
            if game['status'] == 'P':
                pregame_events.append(listitem)
            elif game['status'] == 'I':
                live_events.append(listitem)
            elif game['status'] == 'F':
                final_events.append(listitem)
        except Exception as e:
            Script.log(str(e), lvl=Script.ERROR)

    events = []
    for type in types:
        if type == 'live':
            events.extend(live_events)
        elif type == 'pregame':
            events.extend(pregame_events)
        elif type == 'final':
            events.extend(final_events)

    return events



@Route.register(content_type='videos')
def game_links(plugin, game_id):

    global VIEW_MODE
    VIEW_MODE = '53' # Shift

    response = get(NHL66_API_BASE_URL + NHL66_SCHEDULE_PATH, 'nhl66', skip_cache=True)
    response.raise_for_status()
    state = json.loads(response.text)
    listitems = []
    links = state['links']
    games = state['games']

    # Find the game
    game = None
    for game_i in games:
        try:
            if game_id == game_i['id']:
                game = game_i
                break
        except:
            pass

    # Search for a TheSportsDB event
    tsdb_event = None
    if game:
        try:
            start_datetime = datetime.fromisoformat(game['start_datetime'].replace('Z','+00:00'))
            tsdb_event = get_game(start_datetime, game['home_abr'], game['away_abr'])
        except:
            pass
    
    # Search for TheSportsDV TV Events
    tv_events = None
    if tsdb_event:
        try:
            tv_events = get_tv_events(tsdb_event)
        except:
            pass
    
    # List links
    for link in links:
        try:
            content_id = link['content_id'].split('|')
            if game_id == int(content_id[1].replace('G','')):
                stream = content_id[3]
                label = '{} - {}'.format(link['provider'], stream)
                if link['status'] == 'L':
                    label = f'{bold(color("Live", "limegreen"))} - {label}'
                elif link['status'] == 'R':
                    label = f'{bold(color("Replay", "gold"))} - {label}'
                elif link['status'] == 'E':
                    label = f'{bold(color("Bugged", "crimson"))} - {label}'
                elif link['status'] == 'P':
                    label = f'{bold(color("Planned", "deeppink"))} - {label}'
                # Create the listitem
                listitem = None
                listitem = Listitem.from_dict(play_link, label, params={'link_id': link['id']})
                listitem.label = label
                listitem.info.title = label
                # Set default thumbnails
                thumbnail = None
                if 'nhl' in link['provider'].lower():
                    thumbnail = NHLTV_THUMB
                elif 'espn' in link['provider'].lower():
                    thumbnail = ESPN_THUMB
                # Set custom thumbnails
                if tv_events:
                    for tv_event in tv_events:
                        try:
                            if stream.lower() == 'french':
                                if 'rds' in tv_event['strChannel'].lower():
                                    thumbnail = RDS_THUMB
                                elif 'tva sports' in tv_event['strChannel'].lower():
                                    thumbnail = TVASPORTS_THUMB
                            elif stream.lower() == 'sportsnet':
                                if 'sportsnet' in tv_event['strChannel'].lower():
                                    thumbnail = SPORTSNET_THUMB
                        except:
                            continue
                listitem.art.thumb  = thumbnail
                listitem.art.fanart = thumbnail
                listitem.art.poster = thumbnail
                
                # Add the listitem
                listitems.append(listitem)
        except Exception as e:
            Script.log(e, lvl=Script.WARNING)
            pass
    return listitems



@Resolver.register
def play_link(plugin: Resolver, link_id):
    response = get(NHL66_API_BASE_URL + NHL66_SCHEDULE_PATH, 'nhl66', skip_cache=True)
    response.raise_for_status()
    state = json.loads(response.text)
    links = state['links']
    games = state['games']

    # Find the link
    link = None
    for tlink in links:
        if tlink['id'] == link_id:
            link = tlink
            break
    if link is None:
        raise NotificationError('Parsing Error', 'Cannot find the requested link.')

    # Check if url exists
    if not link['url']:
        raise NotificationError('Unavailable', 'This link is not available yet.')
    
    # Extract infos from the content id
    content_id = link['content_id'].split('|')
    game_id = int(content_id[1].replace('G',''))
    stream_name = content_id[3]

    # Find game associated with the link
    game = None
    for tgame in games:
        if tgame['id'] == game_id:
            game = tgame
            break
    if game is None:
        raise NotificationError('Parsing Error', 'Cannot find the requested game.')

    # Get the provider
    provider = None
    if 'espn' in link['provider'].lower():
        provider = 'espn'
    elif 'nhl' in link['provider'].lower():
        provider = 'nhltv'
    
    # Build the list item
    listitem = Listitem()
    listitem.label = f'{game["away_abr"]} @ {game["home_abr"]} ({stream_name})'
    listitem.set_path(encode_proxy_url(link['url'], provider=provider))
    listitem.listitem.setContentLookup(False)
    listitem.listitem.setMimeType('application/x-mpegURL')
    listitem.listitem.setProperty('inputstream', 'inputstream.adaptive')
    listitem.listitem.setProperty('inputstream.adaptive.manifest_type', 'hls')
    listitem.listitem.setProperty('inputstream.adaptive.stream_selection_type', 'ask-quality')
    return listitem