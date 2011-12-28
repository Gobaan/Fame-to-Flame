import pycurl
from time import time 

def process_wrapper (url, outputs):
  outputs[url] = []
  def store(buf):
    outputs[url] += [buf]
  return store


def parallel_fetch(urls):
  """ 
  Given a set of URLs fetches all of them in parallel and returns
  all the responses at once. We cannot process them in parallel
  because the data is returned as a partial buffer
  """
  m = pycurl.CurlMulti()
  urls = set(urls)
  handles = []
  responses = {}
  for link in urls:
    c = pycurl.Curl()
    c.setopt(pycurl.URL, link.encode('utf-8'))
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.CONNECTTIMEOUT, 30)
    c.setopt(pycurl.TIMEOUT, 300)
    c.setopt(pycurl.NOSIGNAL, 1)
    c.setopt(pycurl.WRITEFUNCTION, process_wrapper(link, responses))
    handles += [c]
    m.add_handle(c)

  num_processed = 0
  start = time()
  while num_processed < len(urls):
    while 1:
      ret, num_handles = m.perform()
      if not ret == pycurl.E_CALL_MULTI_PERFORM: break
    
    while 1:
      num_q, ok_list, err_list = m.info_read()
      for c in ok_list:
        m.remove_handle(c)
        c.close()
        handles.remove(c)

      for c, errno, errmsg in err_list:
        m.remove_handle(c)
        c.close()
        handles.remove(c)
      num_processed += len(ok_list) + len(err_list)

      if num_q == 0: break
    m.select(1.0)
    if time() - start > 30: return {}

  for url in responses:
    responses[url] = ''.join(responses[url])
  return responses

