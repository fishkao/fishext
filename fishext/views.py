from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db import connection
from datetime import datetime, timedelta

def dashboard(request, template_name='fishext/dashboard.html'):
    #return render_to_response(template_name, RequestContext(request))
    params = request.GET if request.method == 'GET' else request.POST
    t_start = (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d 00:00:00")
    t_end = (datetime.now() +  timedelta(days=15)).strftime("%Y-%m-%d 00:00:00")
    start = params.get("start",t_start)
    end = params.get("end",t_end)
    
    data = {}
    data["start"] = start
    data["end"] = end
    cursor = connection.cursor()
    sql_comment = '''
                  select d.username, count(*) as f from reviews_review_comments as a, 
                  reviews_review as b , reviews_comment as c, auth_user as d 
                  where a.review_id=b.id and c.id=a.comment_id and d.id=b.user_id and 
                  b.timestamp >= "%s" and b.timestamp < "%s" 
                  and b.base_reply_to_id is NULL group by d.username order by f DESC;
                  ''' % (start, end)
    cursor.execute(sql_comment)
    comments = cursor.fetchall()
    data['comments'] = comments
    
    sql_bug = '''
          select d.username,count(*) as f from reviews_review_comments as a, 
          reviews_review as b , reviews_comment as c, auth_user as d 
          where a.review_id=b.id and c.id=a.comment_id and d.id=b.user_id 
          and b.timestamp >= "%s" and 
          b.timestamp < "%s" and b.base_reply_to_id is NULL 
          and c.issue_status is not NULL group by d.username order by f DESC;
          ''' % (start, end)
    cursor.execute(sql_bug)
    bugs = cursor.fetchall()
    data['bugs'] = bugs
    
    sql_bug_detail = '''
                     select d.username,TRIM(e.summary),TRIM(c.text) from 
                     reviews_review_comments as a,reviews_review as b , 
                     reviews_comment as c, auth_user as d, reviews_reviewrequest 
                     as e where a.review_id=b.id and c.id=a.comment_id 
                     and d.id=b.user_id and b.review_request_id=e.id and 
                     b.timestamp >= "%s" and b.timestamp < "%s" 
                     and b.base_reply_to_id is NULL and c.issue_status is not NULL 
                     order by summary;
                     ''' %(start, end)
                     
    cursor.execute(sql_bug_detail)
    bug_detail = cursor.fetchall()
    data['bug_detail'] = bug_detail
    
    sql_bug_distri = '''
                     select TRIM(e.summary),count(*) as f from reviews_review_comments as a, 
                     reviews_review as b , reviews_comment as c, auth_user as d, 
                     reviews_reviewrequest as e where a.review_id=b.id and c.id=a.comment_id 
                     and d.id=b.user_id and b.review_request_id=e.id and 
                     b.timestamp >= "%s" and b.timestamp < "%s" 
                     and b.base_reply_to_id is NULL and c.issue_status is not NULL group 
                     by summary order by f DESC;
                     ''' %(start, end)
    cursor.execute(sql_bug_distri)
    bug_distri = cursor.fetchall()
    data['bug_distri'] = bug_distri
    
    return render_to_response(template_name,
                          data,
                          context_instance=RequestContext(request))
