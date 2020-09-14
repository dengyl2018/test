#coding=utf-8
from django.shortcuts import render
 
def runoob(request):
    context          = {}
    context['hello'] = 'Hello World!'
    context['name'] = 'Hello World!name'
    context['num'] = 60
    context['csrf_token'] = 'abcd1234'
    context['places_formset'] = {'management_form': 'test_management_form'}
    context['places_formset'] = [{'name': {'label': 'testtest'}}]
    # PlaceFormSet = formset_factory(PlaceForm, can_delete = True)
    return render(request, 'test.html', context)


def java_string_hashcode(s):
    """
    Args:
        s:  任意string

    Returns: hashcode

    """
    h = 0
    for c in s:
        h = (31 * h + ord(c)) & 0xFFFFFFFF
    return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000


if __name__ == "__main__":
    container_id = "1.opera-7265380-newStpEcho-000-gzhxy.IMQA.gzhxy"
    hostname = "gzhxy-ecom-im161.gzhxy"
    env_id = 726538
    ret = java_string_hashcode('{}_{}_{}'.format(container_id, hostname, env_id))
    print(ret)
    print(abs(ret) % 32)