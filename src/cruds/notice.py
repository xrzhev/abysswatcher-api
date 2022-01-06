import aiohttp

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

import models.certs as cert_model


async def do_notice(db: AsyncSession):

    async def get_notice_data(db: AsyncSession):
        q = select(cert_model.Cert)
        results: Result = await db.execute(q.filter(or_(cert_model.Cert.cert_state == "Expired", cert_model.Cert.cert_state == "Danger")))
        expired_list = []
        danger_list = []
        for result in results.all():
            result = result[0]
            result_dict = {"id" : result.id, "domain" : result.domain, "port" : result.port, "expire_time" : result.expire_time, "update_check_time" : result.update_check_time}
            if result.cert_state == "Expired":
                expired_list.append(result_dict)
            elif result.cert_state == "Danger":
                danger_list.append(result_dict)
        return danger_list, expired_list
    
    # SlackApp webhook URL
    url = None
    danger_notice_strings = ":eyes:*30日以内に失効するSSL証明書*\n"
    expired_notice_strings = ":fire:*失効済みSSL証明書*\n"
  
    danger_hosts, expired_hosts = await get_notice_data(db)

    if len(danger_hosts) == 0:
        danger_notice_strings += "• なし\n"
    else:
        for host in danger_hosts:
            danger_notice_strings += f"• https://{host['domain']}:{host['port']}\n\t• 失効日: {host['expire_time']}\n\t• 最終確認日: {host['update_check_time']}\n"

    if len(expired_hosts) == 0:
        expired_notice_strings += "• なし\n"
    else:
        for host in expired_hosts:
            expired_notice_strings += f"• https://{host['domain']}:{host['port']}\n\t• 失効日: {host['expire_time']}\n\t• 最終確認日: {host['update_check_time']}\n"
    
    payload = {"text": danger_notice_strings + "\n\n" + expired_notice_strings}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            return resp.status
