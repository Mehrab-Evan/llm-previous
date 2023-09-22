import orgdb
import chirpent_no_search
def is_active(session_id, org_url, user_question):
    result = orgdb.get_msg_limit(org_url)

    org_msg_limit = result["msg_limit"]
    org_msg_count = result["msg_count"]

    new_org_msg_count = org_msg_count + 1

    if new_org_msg_count > org_msg_limit:
        return "Your message limit is of {f} messages over", org_msg_limit

    chirpent_no_search.chirpent_no_search(user_question, session_id, org_url)

