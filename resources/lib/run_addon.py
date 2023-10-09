# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# noinspection PyUnresolvedReferences
from codequick import Route, Resolver, Listitem, run
from codequick.utils import urljoin_partial, bold
import urlquick
import xbmcgui
import requests
import json
import base64
from datetime import datetime
from .common.url import encode_proxy_url

# API Constants
NHL66_API_BASE_URL = 'https://api.nhl66.ir'
NHL66_SCHEDULE_PATH = '/api/sport/stateshot'

# Labels Constants
LIVE_EVENTS_LABEL = 30000
LIVE_LABEL = 30001
PREGAME_LABEL = 30002
FINAL_LABEL = 30003





@Route.register
def root(plugin: Route):
    """
    :param Route plugin: The plugin parent object.
    """

    yield Listitem.from_dict(live_events, plugin.localize(LIVE_EVENTS_LABEL))


@Route.register
def live_events(plugin: Route):
    response = requests.get(NHL66_API_BASE_URL + NHL66_SCHEDULE_PATH)
    response.raise_for_status()
    state = json.loads(response.text)
    games = state['games']
    live_events = []
    pregame_events = []
    final_events = []
    for game in games:
        try:
            start_datetime = datetime.fromisoformat(game['start_datetime'].replace('Z','+00:00'))
            
            # Build the label
            label = '{} @ {} - {}'.format(game['away_name'], game['home_name'], start_datetime.astimezone().strftime("%Y/%m/%d - %H:%M"))
            if game['status'] == 'P':
                label = plugin.localize(PREGAME_LABEL) + ' - ' + label
            elif game['status'] == 'I':
                label = plugin.localize(LIVE_LABEL) + ' - ' + label
            elif game['status'] == 'F':
                label = plugin.localize(FINAL_LABEL) + ' - ' + label

            # Create the list item
            listitem = Listitem.from_dict(game_links, label, params={'game_id': game['id']})

            # Add it in the right category
            if game['status'] == 'P':
                pregame_events.append(listitem)
            elif game['status'] == 'I':
                live_events.append(listitem)
            elif game['status'] == 'F':
                final_events.append(listitem)
        except:
            pass
    return [*live_events, *pregame_events, *final_events]



@Route.register
def game_links(plugin, game_id):
    response = requests.get(NHL66_API_BASE_URL + NHL66_SCHEDULE_PATH)
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
    response = requests.get(NHL66_API_BASE_URL + NHL66_SCHEDULE_PATH)
    response.raise_for_status()
    state = json.loads(response.text)
    links = state['links']
    for link in links:
        try:
            if link['id'] == link_id:
                encoded_url = encode_proxy_url(link['url'])
                return plugin.extract_source(encoded_url, 3)
        except Exception as e:
            print (e)
    return []