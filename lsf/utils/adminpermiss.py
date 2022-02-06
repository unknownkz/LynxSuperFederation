from lsf import fed_lynx as next


async def member_permissions(chat_id: int, user_id: int):
    permiss = []
    member = await next.get_chat_member(chat_id, user_id)
    if member.can_post_messages:
        permiss.append("can_post_messages")
    if member.can_edit_messages:
        permiss.append("can_edit_messages")
    if member.can_delete_messages:
        permiss.append("can_delete_messages")
    if member.can_restrict_members:
        permiss.append("can_restrict_members")
    if member.can_promote_members:
        permiss.append("can_promote_members")
    if member.can_change_info:
        permiss.append("can_change_info")
    if member.can_invite_users:
        permiss.append("can_invite_users")
    if member.can_pin_messages:
        permiss.append("can_pin_messages")
    if member.can_manage_voice_chats:
        permiss.append("can_manage_voice_chats")
    return permiss
