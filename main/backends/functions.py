def render_mobile(request, template_name, context):
    from django.shortcuts import render
    import re

    mobile_agent_re = re.compile(r".*(iphone|mobile|android)", re.IGNORECASE)
    if mobile_agent_re.match(request.META['HTTP_USER_AGENT']):
        context['is_mobile'] = True

    return render(request, template_name, context)
