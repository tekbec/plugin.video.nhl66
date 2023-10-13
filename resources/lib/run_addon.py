# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# noinspection PyUnresolvedReferences
from codequick import Route, Resolver, Script, Listitem, run
from codequick.utils import bold, color, italic
import json
from datetime import datetime
from .common.url import encode_proxy_url
from .common.requests import get
from .platforms.thesportsdb.schedule import get_game
from .platforms.thesportsdb.tvevents import get_tv_events
import traceback

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





@Route.register
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


@Route.register()
def get_games(plugin: Route, types: list):
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
            image = None

            # Search TheSportsDB thumbnail
            thesportsdb_event = get_game(start_datetime, game['home_abr'], game['away_abr'])
            if thesportsdb_event:
                image = thesportsdb_event['strThumb']
            
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
            if image:
                listitem.art.poster = image

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



@Route.register
def game_links(plugin, game_id):
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
                # Set the provider
                provider = None
                if 'espn' in link['provider'].lower():
                    provider = 'espn'
                elif 'nhl' in link['provider'].lower():
                    provider = 'nhltv'
                # Create the listitem
                listitem = None
                if link['url']:
                    listitem = Listitem()
                    listitem.set_path(encode_proxy_url(link['url'], provider=provider))
                    listitem.label = label
                    listitem.info.title = label
                    listitem.listitem.setContentLookup(False)
                    listitem.listitem.setMimeType('application/x-mpegURL')
                    listitem.listitem.setProperty('inputstream', 'inputstream.adaptive')
                    listitem.listitem.setProperty('inputstream.adaptive.manifest_type', 'hls')
                    listitem.listitem.setProperty('inputstream.adaptive.stream_selection_type', 'ask-quality')
                else:
                    listitem = Listitem.from_dict(play_link, label, params={'link_id': link['id']})
                    listitem.label = label
                    listitem.info.title = label
                # Set default thumbnails
                if provider == 'nhltv':
                    listitem.art.poster = NHLTV_THUMB
                elif provider == 'espn':
                    listitem.art.poster = ESPN_THUMB
                # Set custom thumbnails
                if tv_events:
                    for tv_event in tv_events:
                        try:
                            if stream.lower() == 'french':
                                if 'rds' in tv_event['strChannel'].lower():
                                    listitem.art.poster = RDS_THUMB
                                elif 'tva sports' in tv_event['strChannel'].lower():
                                    listitem.art.poster = TVASPORTS_THUMB
                            elif stream.lower() == 'sportsnet':
                                if 'sportsnet' in tv_event['strChannel'].lower():
                                    listitem.art.poster = SPORTSNET_THUMB
                        except:
                            continue
                
                # Add the listitem
                listitems.append(listitem)
        except Exception as e:
            Script.log(e, lvl=Script.WARNING)
            pass
    return listitems



@Resolver.register
def play_link(plugin: Resolver, link_id):
    response = get(NHL66_API_BASE_URL + NHL66_SCHEDULE_PATH, 'nhl66')
    response.raise_for_status()
    state = json.loads(response.text)
    links = state['links']
    for link in links:
        try:
            if link['id'] == link_id:
                provider = None
                if 'espn' in link['provider'].lower():
                    provider = 'espn'
                elif 'nhl' in link['provider'].lower():
                    provider = 'nhltv'
                encoded_url = encode_proxy_url(link['url'], provider=provider)
                return plugin.extract_source(encoded_url, 3)
        except Exception as e:
            Script.log(str(e), lvl=Script.ERROR)
    return []