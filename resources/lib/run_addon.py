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

# API Constants
NHL66_API_BASE_URL = 'https://api.nhl66.ir'
NHL66_SCHEDULE_PATH = '/api/sport/stateshot'

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
    live_events_label = color(bold(plugin.localize(LIVE_EVENTS_LABEL)), 'crimson')
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
                label = f'{color(bold(plugin.localize(PREGAME_LABEL)), "limegreen")} - {label}'
            elif game['status'] == 'I':
                label = f'{color(bold(plugin.localize(LIVE_LABEL)), "crimson")} - {label}'
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
    response = get(NHL66_API_BASE_URL + NHL66_SCHEDULE_PATH, 'nhl66')
    response.raise_for_status()
    state = json.loads(response.text)
    links = state['links']
    for link in links:
        try:
            content_id = link['content_id'].split('|')
            if game_id == int(content_id[1].replace('G','')):
                stream = content_id[3]
                label = '{} - {}'.format(link['provider'], stream)
                if link['status'] == 'L':
                    label = 'Live - ' + label
                listitem = Listitem()
                listitem.set_path(encode_proxy_url(link['url']))
                listitem.label = label
                listitem.listitem.setContentLookup(False)
                listitem.listitem.setMimeType('application/x-mpegURL')
                listitem.listitem.setProperty('inputstream', 'inputstream.adaptive')
                listitem.listitem.setProperty('inputstream.adaptive.manifest_type', 'hls')
                listitem.listitem.setProperty('inputstream.adaptive.stream_selection_type', 'ask-quality')
                yield listitem
        except:
            pass
    return []



@Resolver.register
def play_link(plugin: Resolver, link_id):
    response = get(NHL66_API_BASE_URL + NHL66_SCHEDULE_PATH, 'nhl66')
    response.raise_for_status()
    state = json.loads(response.text)
    links = state['links']
    for link in links:
        try:
            if link['id'] == link_id:
                encoded_url = encode_proxy_url(link['url'])
                return plugin.extract_source(encoded_url, 3)
        except Exception as e:
            Script.log(str(e), lvl=Script.ERROR)
    return []