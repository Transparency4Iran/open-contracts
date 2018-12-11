from .models import *
from omid_utils.standard import standard_persian


def get_or_create_organizations(non_split):
    sp = non_split.split('/')
    orgs = []
    father = None
    for i in range(0, len(sp) - 1):
        if i == 0:
            father, created = Organization.objects.get_or_create(name=standard_persian(sp[0]))
            orgs.append(father)
        child, created = Organization.objects.get_or_create(name=standard_persian(sp[i + 1]), father=father)
        orgs.append(child)
        father = child
    return orgs[0], orgs[-1]
