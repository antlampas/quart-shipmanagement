#Licensed under the Open Software License version 3.0

#Author:     antlampas
#Created on: 2025-05-15

from quart import session
from quart import render_template
async def standardReturn(template="index.html",sectionName="Home Page",**kwargs):
    if 'auth_token' in session:
        return await render_template(template,SECTIONNAME=sectionName,SESSION=session,**kwargs)
    else:
        return await render_template(template,SECTIONNAME=sectionName,**kwargs)
