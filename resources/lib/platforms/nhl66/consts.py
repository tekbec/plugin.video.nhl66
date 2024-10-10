from .team import Team

# API
API_BASE_URL   = 'https://api.nhl66.ir'
STATESHOT_PATH = '/api/sport/stateshot'
PREMIUM_ACCOUNT_API_BASE_URL = 'https://account24network.com'
SIGNATURE_PATH               = '/api/profile/generate_entitlement_signature'
INFO_PATH                    = '/api/profile/get_premium_code'
PREMIUM_NHL_API_BASE_URL     = 'https://api.nhl24network.com'
STREAM_INFO_PATH             = '/api/generate_stream_info'
PREMIUM_ORIGIN = 'https://nhl24network.com'

# Thumbnails
NHLTV_THUMB     = 'https://i.imgur.com/HGsNesm.png'
ESPN_THUMB      = 'https://i.imgur.com/09KBp1W.png'
TVASPORTS_THUMB = 'https://i.imgur.com/lonf7w3.png'
RDS_THUMB       = 'https://i.imgur.com/qhrFsYh.png'
SPORTSNET_THUMB = 'https://i.imgur.com/qB7bKBT.png'

# Labels
LIVE_EVENTS_LABEL = 30000
LIVE_LABEL = 30001
PREGAME_LABEL = 30002
FINAL_LABEL = 30003
REPLAY_LABEL = 30004

# Teams
TEAMS = [
    Team(abbreviation='ana', city='Anaheim',      name='Ducks',          country='US', tsdb_id='134846', logo_light_url='https://assets.nhle.com/logos/nhl/svg/ANA_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/ANA_dark.svg'),
    Team(abbreviation='ari', city='Arizona',      name='Coyotes',        country='US', tsdb_id='134847', logo_light_url='https://assets.nhle.com/logos/nhl/svg/ARI_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/ARI_dark.svg'),
    Team(abbreviation='bos', city='Boston',       name='Bruins',         country='US', tsdb_id='134830', logo_light_url='https://assets.nhle.com/logos/nhl/svg/BOS_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/BOS_dark.svg'),
    Team(abbreviation='buf', city='Buffalo',      name='Sabres',         country='US', tsdb_id='134831', logo_light_url='https://assets.nhle.com/logos/nhl/svg/BUF_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/BUF_dark.svg'),
    Team(abbreviation='car', city='Carolina',     name='Hurricanes',     country='US', tsdb_id='134838', logo_light_url='https://assets.nhle.com/logos/nhl/svg/CAR_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/CAR_dark.svg'),
    Team(abbreviation='cbj', city='Columbus',     name='Blue Jackets',   country='US', tsdb_id='134839', logo_light_url='https://assets.nhle.com/logos/nhl/svg/CBJ_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/CBJ_dark.svg'),
    Team(abbreviation='cgy', city='Calgary',      name='Flames',         country='CA', tsdb_id='134848', logo_light_url='https://assets.nhle.com/logos/nhl/svg/CGY_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/CGY_dark.svg'),
    Team(abbreviation='chi', city='Chicago',      name='Blackhawks',     country='US', tsdb_id='134854', logo_light_url='https://assets.nhle.com/logos/nhl/svg/CHI_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/CHI_dark.svg'),
    Team(abbreviation='col', city='Colorado',     name='Avalanche',      country='US', tsdb_id='134855', logo_light_url='https://assets.nhle.com/logos/nhl/svg/COL_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/COL_dark.svg'),
    Team(abbreviation='dal', city='Dallas',       name='Stars',          country='US', tsdb_id='134856', logo_light_url='https://assets.nhle.com/logos/nhl/svg/DAL_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/DAL_dark.svg'),
    Team(abbreviation='det', city='Detroit',      name='Red Wings',      country='US', tsdb_id='134832', logo_light_url='https://assets.nhle.com/logos/nhl/svg/DET_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/DET_dark.svg'),
    Team(abbreviation='edm', city='Edmonton',     name='Oilers',         country='CA', tsdb_id='134849', logo_light_url='https://assets.nhle.com/logos/nhl/svg/EDM_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/EDM_dark.svg'),
    Team(abbreviation='fla', city='Florida',      name='Panthers',       country='US', tsdb_id='134833', logo_light_url='https://assets.nhle.com/logos/nhl/svg/FLA_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/FLA_dark.svg'),     
    Team(abbreviation='lak', city='Los Angeles',  name='Kings',          country='US', tsdb_id='134852', logo_light_url='https://assets.nhle.com/logos/nhl/svg/LAK_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/LAK_dark.svg'),    
    Team(abbreviation='min', city='Minnesota',    name='Wild',           country='US', tsdb_id='134857', logo_light_url='https://assets.nhle.com/logos/nhl/svg/MIN_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/MIN_dark.svg'),       
    Team(abbreviation='mtl', city='Montreal',     name='Canadiens',      country='CA', tsdb_id='134834', logo_light_url='https://assets.nhle.com/logos/nhl/svg/MTL_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/MTL_dark.svg'),   
    Team(abbreviation='njd', city='New Jersey',   name='Devils',         country='US', tsdb_id='134840', logo_light_url='https://assets.nhle.com/logos/nhl/svg/NJD_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/NJD_dark.svg'),    
    Team(abbreviation='nsh', city='Nashville',    name='Predators',      country='US', tsdb_id='134858', logo_light_url='https://assets.nhle.com/logos/nhl/svg/NSH_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/NSH_dark.svg'),  
    Team(abbreviation='nyi', city='New York',     name='Islanders',      country='US', tsdb_id='134841', logo_light_url='https://assets.nhle.com/logos/nhl/svg/NYI_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/NYI_dark.svg'),   
    Team(abbreviation='nyr', city='New York',     name='Rangers',        country='US', tsdb_id='134842', logo_light_url='https://assets.nhle.com/logos/nhl/svg/NYR_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/NYR_dark.svg'),     
    Team(abbreviation='ott', city='Ottawa',       name='Senators',       country='CA', tsdb_id='134835', logo_light_url='https://assets.nhle.com/logos/nhl/svg/OTT_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/OTT_dark.svg'),      
    Team(abbreviation='phi', city='Philadelphia', name='Flyers',         country='US', tsdb_id='134843', logo_light_url='https://assets.nhle.com/logos/nhl/svg/PHI_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/PHI_dark.svg'),  
    Team(abbreviation='pit', city='Pittsburgh',   name='Penguins',       country='US', tsdb_id='134844', logo_light_url='https://assets.nhle.com/logos/nhl/svg/PIT_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/PIT_dark.svg'),  
    Team(abbreviation='sea', city='Seattle',      name='Kraken',         country='US', tsdb_id='140082', logo_light_url='https://assets.nhle.com/logos/nhl/svg/SEA_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/SEA_dark.svg'),       
    Team(abbreviation='sjs', city='San Jose',     name='Sharks',         country='US', tsdb_id='134853', logo_light_url='https://assets.nhle.com/logos/nhl/svg/SJS_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/SJS_dark.svg'),      
    Team(abbreviation='stl', city='St. Louis',    name='Blues',          country='US', tsdb_id='134859', logo_light_url='https://assets.nhle.com/logos/nhl/svg/STL_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/STL_dark.svg'),      
    Team(abbreviation='tbl', city='Tampa Bay',    name='Lightning',      country='US', tsdb_id='134836', logo_light_url='https://assets.nhle.com/logos/nhl/svg/TBL_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/TBL_dark.svg'),  
    Team(abbreviation='tor', city='Toronto',      name='Maple Leafs',    country='CA', tsdb_id='134837', logo_light_url='https://assets.nhle.com/logos/nhl/svg/TOR_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/TOR_dark.svg'),  
    Team(abbreviation='uta', city='Utah',         name='Hockey Club',    country='US', tsdb_id='148494', logo_light_url='https://assets.nhle.com/logos/nhl/svg/UTA_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/UTA_dark.svg'),  
    Team(abbreviation='van', city='Vancouver',    name='Canucks',        country='CA', tsdb_id='134850', logo_light_url='https://assets.nhle.com/logos/nhl/svg/VAN_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/VAN_dark.svg'),    
    Team(abbreviation='vgk', city='Vegas',        name='Golden Knights', country='US', tsdb_id='135913', logo_light_url='https://assets.nhle.com/logos/nhl/svg/VGK_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/VGK_dark.svg'), 
    Team(abbreviation='wpg', city='Winnipeg',     name='Jets',           country='CA', tsdb_id='134851', logo_light_url='https://assets.nhle.com/logos/nhl/svg/WPG_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/WPG_dark.svg'),        
    Team(abbreviation='wsh', city='Washington',   name='Capitals',       country='US', tsdb_id='134845', logo_light_url='https://assets.nhle.com/logos/nhl/svg/WSH_light.svg', logo_dark_url='https://assets.nhle.com/logos/nhl/svg/WSH_dark.svg')  

]