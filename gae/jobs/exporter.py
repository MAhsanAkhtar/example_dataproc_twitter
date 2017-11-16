#MIT License
#
#Copyright (c) 2017 Willian Fuks
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


import datetime

from google.appengine.api import taskqueue
import utils


class ExporterJob(object):
    """Job that runs queued tasks."""
    def __init__(self):
        self.task = None


    def run(self, args): 
        """Executes the job.

        :type args: dict
        :param args: dictionary with arguments to setup the job. This parameter
                     comes from the input request.

          :type args.url: str
          :param args.url: which URL to invoke to run queue task.

          :type args.target: str
          :param args.target: service where to make the URL request.

          :param args.{params}: every parameter other then ``url`` and 
                                ``target`` that is sent as param in the POST
                                request. 
        """
        url = args.pop('url') 
        target = args.pop('target')
        task = taskqueue.add(url=url, target=target, params=args)
        self.task = task
 

    def _process_date(date):
        """Process the date variable from URL. Processing it is a bit more
        demanding as there's some rules applied such as one for a defined
        date and one for when date is None.

        :type date: str
        :param date: date to process the export in BigQuery.

        :rtype date: str
        :returns: date processed in format %Y-%m-%d.
        """
        if not date:
            date = utils.get_yesterday_date().strftime('%Y-%m-%d') 
        else:
            date = utils.process_url_date(date)
        return date


    def __str__(self):
        if not self.task:
            return 'No task has been enqueued so far'
        return "Task {} enqued, ETA {}".format(self.task.name, self.task.eta) 
