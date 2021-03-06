import json

import kopf

from grafana import api, organization, user


@kopf.on.create('grafana.k8spin.cloud', 'v1', 'organizations')
def create_organization(spec, meta, **kwargs):
    name = meta.get('name')
    datasources = spec.get('datasources', list())
    dashboards = spec.get('dashboards', list())
    return organization.create(api, name, datasources, dashboards)


@kopf.on.update('grafana.k8spin.cloud', 'v1', 'organizations')
def update_organization(old, new, status, **kwargs):
    orgId = status['create_organization']['orgId']
    oldDataSources = old.get('spec').get('datasources', list())
    newDataSources = new.get('spec').get('datasources', list())
    oldDashboards = old.get('spec').get('dashboards', list())
    newDashboards = new.get('spec').get('dashboards', list())
    organization.update(api, orgId, oldDataSources,
                        newDataSources, oldDashboards, newDashboards)


@kopf.on.delete('grafana.k8spin.cloud', 'v1', 'organizations')
def delete_organization(status, **kwargs):
    return organization.delete(api, status['create_organization']['orgId'])


@kopf.on.create('grafana.k8spin.cloud', 'v1', 'users')
def create_user(spec, meta, **kwargs):
    name = meta.get('name')
    email = spec.get('email')
    organizationNames = spec.get('organizations', list())
    return user.create(api, name, email, organizationNames)


@kopf.on.update('grafana.k8spin.cloud', 'v1', 'users')
def update_user(status, spec, meta, old, new, **kwargs):
    oldOrganizationNames = old.get('spec').get('organizations', list())
    newOrganizationNames = new.get('spec').get('organizations', list())
    userId = status['create_user']['id']
    name = meta.get('name')
    email = spec.get('email')
    return user.update(api, userId, name, email, oldOrganizationNames, newOrganizationNames)


@kopf.on.delete('grafana.k8spin.cloud', 'v1', 'users')
def delete_user(status, **kwargs):
    return user.delete(api, status['create_user']['id'])
