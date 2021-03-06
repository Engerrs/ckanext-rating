import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.rating.logic import action
from ckanext.rating import helpers
import ckanext.rating.logic.auth as rating_auth

class RatingPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IAuthFunctions)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'rating')
        toolkit.add_resource('public/css/', 'rating_css')
        toolkit.add_resource('public/js/', 'rating_js')

    # IActions

    def get_actions(self):
        return {
            'rating_package_create': action.rating_package_create,
            'rating_package_get': action.rating_package_get,
            'rating_showcase_create': action.rating_package_create,
            'rating_showcase_get': action.rating_package_get
        }

    ## ITemplateHelpers

    def get_helpers(self):
        return {
            'package_rating': action.rating_package_get,
            'get_user_rating': helpers.get_user_rating
        }

    # IAuthFunctions

    def get_auth_functions(self):
        return rating_auth.get_rating_auth_dict()

    # IRoutes

    def before_map(self, map):
        map.connect('/rating/dataset/:package/:rating',
                    controller='ckanext.rating.controller:RatingController',
                    action='submit_package_rating')

        map.connect('/rating/showcase/:package/:rating',
                    controller='ckanext.rating.controller:RatingController',
                    action='submit_showcase_rating')

        return map
