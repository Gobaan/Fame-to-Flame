"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    map.connect('/', controller='metasearch', action='index')
    map.connect('/search', controller='metasearch', action='custom')
    map.connect('/custom', controller='metasearch', action='custom')
    map.connect('/polarize', controller='metasearch', action='polarize')
    map.connect('/analysis', controller='metasearch', action='analysis')

    map.connect('/getasyncresults', controller='metasearch', action='getasyncresults')

    #map.connect('/', controller='hello', action='index')
    #map.connect('/search', controller='hello', action='search')
    #map.connect('/polarize', controller='hello', action='polarize')
    #map.connect('/custom', controller='hello', action='custom')
    #map.connect('/analysis', controller='hello', action='analysis')

    map.connect('/feedback', controller='hello', action='feedback')

    return map
