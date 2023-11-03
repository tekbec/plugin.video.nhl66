proxies_providers = {
    'torguard': {
        'id': 'torguard',
        'name': 'TorGuard',
        'type': 'https',
        'credentials_required': True,
        'locations': {
            'br': {
                'id': 'br',
                'country': 'Brazil',
                'city': 'Sau Paulo',
                'suffix': 'LOC1',
                'hostname': 'br.secureconnect.me',
                'port': 7070
            },
            'br2': {
                'id': 'br2',
                'country': 'Brazil',
                'city': 'Sau Paulo',
                'suffix': 'LOC2',
                'hostname': 'br2.secureconnect.me',
                'port': 7070
            },
            'ch': {
                'id': 'ch',
                'country': 'Chile',
                'city': 'Vina del Mar',
                'hostname': 'ch.secureconnect.me',
                'port': 7070
            },
            'ca': {
                'id': 'ca',
                'country': 'Canada',
                'city': 'Toronto',
                'hostname': 'ca.secureconnect.me',
                'port': 7070
            },
            'camtl': {
                'id': 'camtl',
                'country': 'Canada',
                'city': 'Montréal',
                'hostname': 'camtl.secureconnect.me',
                'port': 7070
            },
            'cavan': {
                'id': 'cavan',
                'country': 'Canada',
                'city': 'Vancouver',
                'hostname': 'cavan.secureconnect.me',
                'port': 7070
            },
            'mx': {
                'id': 'mx',
                'country': 'Mexico',
                'city': 'Mexico City',
                'hostname': 'mx.secureconnect.me',
                'port': 7070
            },
            'us-atl': {
                'id': 'us-atl',
                'country': 'United States',
                'city': 'Atlanta',
                'hostname': 'us-atl.secureconnect.me',
                'port': 7070
            },
            'us-la': {
                'id': 'us-la',
                'country': 'United States',
                'city': 'Los Angeles',
                'hostname': 'us-la.secureconnect.me',
                'port': 7070
            },
            'us-fl': {
                'id': 'us-fl',
                'country': 'United States',
                'city': 'Miami',
                'hostname': 'us-fl.secureconnect.me',
                'port': 7070
            },
            'us-den': {
                'id': 'us-den',
                'country': 'United States',
                'city': 'Denver',
                'hostname': 'us-den.secureconnect.me',
                'port': 7070
            },
            'us-hou': {
                'id': 'us-hou',
                'country': 'United States',
                'city': 'Houston',
                'hostname': 'us-hou.secureconnect.me',
                'port': 7070
            },
            'us-dal': {
                'id': 'us-dal',
                'country': 'United States',
                'city': 'Dallas',
                'suffix': 'LOC1',
                'hostname': 'us-dal.secureconnect.me',
                'port': 7070
            },
            'us-dal-loc2': {
                'id': 'us-dal-loc2',
                'country': 'United States',
                'city': 'Dallas',
                'suffix': 'LOC2',
                'hostname': 'us-dal-loc2.secureconnect.me',
                'port': 7070
            },
            'us-nj': {
                'id': 'us-nj',
                'country': 'United States',
                'city': 'New Jersey',
                'suffix': 'LOC1',
                'hostname': 'us-nj.secureconnect.me',
                'port': 7070
            },
            'us-nj-loc2': {
                'id': 'us-nj-loc2',
                'country': 'United States',
                'city': 'New Jersey',
                'suffix': 'LOC2',
                'hostname': 'us-nj-loc2.secureconnect.me',
                'port': 7070
            },
            'us-ny': {
                'id': 'us-ny',
                'country': 'United States',
                'city': 'New York',
                'hostname': 'us-ny.secureconnect.me',
                'port': 7070
            },
            'us-chi': {
                'id': 'us-chi',
                'country': 'United States',
                'city': 'Chicago',
                'suffix': 'LOC1',
                'hostname': 'us-chi.secureconnect.me',
                'port': 7070
            },
            'us-chi-loc2': {
                'id': 'us-chi-loc2',
                'country': 'United States',
                'city': 'Chicago',
                'suffix': 'LOC2',
                'hostname': 'us-chi-loc2.secureconnect.me',
                'port': 7070
            },
            'us-lv': {
                'id': 'us-lv',
                'country': 'United States',
                'city': 'Las Vegas',
                'hostname': 'us-lv.secureconnect.me',
                'port': 7070
            },
            'us-sf': {
                'id': 'us-sf',
                'country': 'United States',
                'city': 'San Francisco',
                'hostname': 'us-sf.secureconnect.me',
                'port': 7070
            },
            'us-sa': {
                'id': 'us-sa',
                'country': 'United States',
                'city': 'Seattle',
                'hostname': 'us-sa.secureconnect.me',
                'port': 7070
            },
            'us-slc': {
                'id': 'us-slc',
                'country': 'United States',
                'city': 'Salt Lake City',
                'hostname': 'us-slc.secureconnect.me',
                'port': 7070
            },
            'aus': {
                'id': 'aus',
                'country': 'Austria',
                'city': 'Vienna',
                'hostname': 'aus.secureconnect.me',
                'port': 7070
            },
            'bg': {
                'id': 'bg',
                'country': 'Belgium',
                'city': 'Brussels',
                'hostname': 'bg.secureconnect.me',
                'port': 7070
            },
            'bul': {
                'id': 'bul',
                'country': 'Bulgaria',
                'city': 'Sofia',
                'hostname': 'bul.secureconnect.me',
                'port': 7070
            },
            'cz': {
                'id': 'cz',
                'country': 'Czech Republic',
                'city': 'Prague',
                'hostname': 'cz.secureconnect.me',
                'port': 7070
            },
            'dn': {
                'id': 'dn',
                'country': 'Denmark',
                'city': 'Copenhagen',
                'hostname': 'dn.secureconnect.me',
                'port': 7070
            },
            'fn': {
                'id': 'fn',
                'country': 'Finland',
                'city': 'Helsinki',
                'hostname': 'fn.secureconnect.me',
                'port': 7070
            },
            'fr': {
                'id': 'fr',
                'country': 'France',
                'city': 'Paris',
                'hostname': 'fr.secureconnect.me',
                'port': 7070
            },
            'ger': {
                'id': 'ger',
                'country': 'Germany',
                'city': 'Frankfurt',
                'hostname': 'ger.secureconnect.me',
                'port': 7070
            },
            'gre': {
                'id': 'gre',
                'country': 'Greece',
                'city': 'Athens',
                'hostname': 'gre.secureconnect.me',
                'port': 7070
            },
            'hg': {
                'id': 'hg',
                'country': 'Hungary',
                'city': 'Budapest',
                'hostname': 'hg.secureconnect.me',
                'port': 7070
            },
            'ice': {
                'id': 'ice',
                'country': 'Iceland',
                'city': 'Reykjavik',
                'hostname': 'ice.secureconnect.me',
                'port': 7070
            },
            'ire': {
                'id': 'ire',
                'country': 'Ireland',
                'city': 'Dublin',
                'hostname': 'ire.secureconnect.me',
                'port': 7070
            },
            'it': {
                'id': 'it',
                'country': 'Italy',
                'city': 'Milan',
                'hostname': 'it.secureconnect.me',
                'port': 7070
            },
            'md': {
                'id': 'md',
                'country': 'Moldova',
                'city': 'Chisinau',
                'hostname': 'md.secureconnect.me',
                'port': 7070
            },
            'nl': {
                'id': 'nl',
                'country': 'Netherlands',
                'city': 'Amsterdam',
                'hostname': 'nl.secureconnect.me',
                'port': 7070
            },
            'no': {
                'id': 'no',
                'country': 'Norway',
                'city': 'Oslo',
                'hostname': 'no.secureconnect.me',
                'port': 7070
            },
            'pl': {
                'id': 'pl',
                'country': 'Poland',
                'city': 'Warsaw',
                'hostname': 'pl.secureconnect.me',
                'port': 7070
            },
            'pg': {
                'id': 'pg',
                'country': 'Portugal',
                'city': 'Lisbon',
                'hostname': 'pg.secureconnect.me',
                'port': 7070
            },
            'ro': {
                'id': 'ro',
                'country': 'Romania',
                'city': 'Bucharest',
                'hostname': 'ro.secureconnect.me',
                'port': 7070
            },
            'ru': {
                'id': 'ru',
                'country': 'Russia',
                'city': 'Moscow',
                'hostname': 'ru.secureconnect.me',
                'port': 7070
            },
            'serbia': {
                'id': 'serbia',
                'country': 'Serbia',
                'city': 'Belgrade',
                'hostname': 'serbia.secureconnect.me',
                'port': 7070
            },
            'slk': {
                'id': 'slk',
                'country': 'Slovakia',
                'city': 'Bratislava',
                'hostname': 'slk.secureconnect.me',
                'port': 7070
            },
            'sp': {
                'id': 'sp',
                'country': 'Spain',
                'city': 'Madrid',
                'hostname': 'sp.secureconnect.me',
                'port': 7070
            },
            'swe': {
                'id': 'swe',
                'country': 'Sweden',
                'city': 'Stockholm',
                'hostname': 'swe.secureconnect.me',
                'port': 7070
            },
            'swiss': {
                'id': 'swiss',
                'country': 'Switzerland',
                'city': 'Zurich',
                'hostname': 'swiss.secureconnect.me',
                'port': 7070
            },
            'tk': {
                'id': 'tk',
                'country': 'Turkey',
                'city': 'Istanbul',
                'hostname': 'tk.secureconnect.me',
                'port': 7070
            },
            'ukr': {
                'id': 'ukr',
                'country': 'Ukraine',
                'city': 'Kyiv',
                'hostname': 'ukr.secureconnect.me',
                'port': 7070
            },
            'uk.man': {
                'id': 'uk.man',
                'country': 'United Kingdom',
                'city': 'Manchester',
                'hostname': 'uk.man.secureconnect.me',
                'port': 7070
            },
            'uk': {
                'id': 'uk',
                'country': 'London',
                'city': 'Manchester',
                'hostname': 'uk.secureconnect.me',
                'port': 7070
            },
            'au': {
                'id': 'au',
                'country': 'Australia',
                'city': 'Sydney',
                'hostname': 'au.secureconnect.me',
                'port': 7070
            },
            'hk': {
                'id': 'hk',
                'country': 'Hong Kong',
                'city': 'Hong Kong',
                'hostname': 'hk.secureconnect.me',
                'port': 7070
            },
            'id': {
                'id': 'id',
                'country': 'Indonesia',
                'city': 'Jakarta',
                'hostname': 'id.secureconnect.me',
                'port': 7070
            },
            'jp': {
                'id': 'jp',
                'country': 'Japan',
                'city': 'Tokyo',
                'hostname': 'jp.secureconnect.me',
                'port': 7070
            },
            'sk': {
                'id': 'sk',
                'country': 'South Korea',
                'city': 'Seoul',
                'hostname': 'sk.secureconnect.me',
                'port': 7070
            },
            'nz': {
                'id': 'nz',
                'country': 'New Zealand',
                'city': 'Auckland',
                'hostname': 'nz.secureconnect.me',
                'port': 7070
            },
            'sg': {
                'id': 'sg',
                'country': 'Singapore',
                'city': 'Singapore',
                'hostname': 'sg.secureconnect.me',
                'port': 7070
            },
            'tw': {
                'id': 'tw',
                'country': 'Taiwan',
                'city': 'Taipei',
                'hostname': 'tw.secureconnect.me',
                'port': 7070
            },
            'th': {
                'id': 'th',
                'country': 'Thailand',
                'city': 'Bangkok',
                'hostname': 'th.secureconnect.me',
                'port': 7070
            },
            'bh': {
                'id': 'bh',
                'country': 'Bahrain',
                'city': 'Manama',
                'hostname': 'bh.secureconnect.me',
                'port': 7070
            },
            'in': {
                'id': 'in',
                'country': 'India',
                'city': 'Mumbai',
                'hostname': 'in.secureconnect.me',
                'port': 7070
            },
            'isr-loc1': {
                'id': 'isr-loc1',
                'country': 'Israel',
                'city': 'Tel Aviv',
                'hostname': 'isr-loc1.secureconnect.me',
                'port': 7070
            },
            'isr-loc2': {
                'id': 'isr-loc2',
                'country': 'Israel',
                'city': 'Petah Tikva',
                'hostname': 'isr-loc2.secureconnect.me',
                'port': 7070
            },
            'sa': {
                'id': 'sa',
                'country': 'South Africa',
                'city': 'Johannesburg',
                'hostname': 'sa.secureconnect.me',
                'port': 7070
            },
            'uae': {
                'id': 'uae',
                'country': 'United Arab Emirates',
                'city': 'Dubai',
                'hostname': 'uae.secureconnect.me',
                'port': 7070
            },
        },

    }
}