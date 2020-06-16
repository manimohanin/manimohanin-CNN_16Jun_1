from typing import Dict, List

html_text = '''<td>
<div class="curvedbox">
<span id="user-id" class=udata>__USER_DOMAIN__\__USER_NAME__</span>
<br>
<br>
<b>Workspace Id :</b> <span id="ws-id" class=udata>__WORKSPACE_ID__</span><br>
<b>Computer Name :</b> <span class=udata>__COMPUTER_NAME__</span><br>
<b>Compute Type :</b> <span class=udata>__COMPUTE_TYPE__</span><br>
<b>Location :</b> <span class=udata>us-west-2 (Oregon)</span><br>
<b>Registration Code :</b> <span class=udata>__REGISTRATION_CODE__</span><br>
<b>IP Address :</b> <span class=udata>__IP_ADDRESS__</span><br style="line-height: 25px;">
<b class="ball __COLOR_BALL__">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span id="ws-state">__WORKSPACE_STATE__</span></b><br>
<br>
<button class="base_btn __COLOR_BUTTON__" id=rebootbtn>__BUTTON_TEXT__</button><br>
<span id=reboot_result></span>
</div>
<div id="dialog-confirm" title="Reboot WorkSpace">
<span id="dialog-warning-icon"></span><br>
<span id="dialog-warning-msg"></span><br><br>
<span id="dialog-ws-user-id"></span>
</div>
<script>
setTimeout(session_expired, __SESSION_TIMEOUT__);
</script>
</td>'''
html_body = """"""
cnt = 0
cnt = cnt + 1
html_text = html_text.replace("user-id", "user-id"+str(cnt), 1)
html_text = html_text.replace("ws-id", "ws-id"+str(cnt), 1)
html_text = html_text.replace("ws-state", "ws-state"+str(cnt), 1)
html_text = html_text.replace("reboot_result", "reboot_result"+str(cnt), 1)
html_text = html_text.replace("dialog-confirm", "dialog-confirm"+str(cnt), 1)
html_text = html_text.replace("dialog-warning-icon", "dialog-warning-icon"+str(cnt), 1)
html_text = html_text.replace("dialog-warning-msg", "dialog-warning-msg"+str(cnt), 1)
html_text = html_text.replace("dialog-ws-user-id", "dialog-ws-user-id"+str(cnt), 1)

html_body = """"""
if not html_body:
    print('Divided')
else:
    print('ELSE')
html_body = html_body + html_text
#print(html_body)

neg = {'transit': 'us-west-1', 'infect': 'us-west-1', 'spam': 'us-west-2'}


for k, v in neg.items():

    print(k, v)