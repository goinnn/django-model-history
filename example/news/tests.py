# -*- coding: utf-8 -*-
# Copyright (c) 2015 by Pablo Martín <goinnn@gmail.com>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.
import datetime

from django.test import TestCase

from news.models import NewsItem, NewsItemHistory


class NewsModelHistoryTestCase(TestCase):

    def test_1_insert(self):
        news_item_count = NewsItem.objects.count()
        news_item_history_count = NewsItemHistory.objects.count()
        self.assertEqual(news_item_count, 0)
        self.assertEqual(news_item_history_count, 0)
        news_item = NewsItem.objects.create(title='My first news item',
                                            publish_date=datetime.datetime.now())

        news_item_count = NewsItem.objects.count()
        news_item_history_count = NewsItemHistory.objects.count()
        self.assertEqual(news_item_count, 1)
        self.assertEqual(news_item_history_count, 1)

        news_item = NewsItem.objects.get(pk=1)
        news_item_history = NewsItemHistory.objects.get(history=news_item)
        self.assertEqual(news_item.title, news_item_history.title)
        self.assertEqual(news_item.description, news_item_history.description)
        self.assertEqual(news_item.publish_date, news_item_history.publish_date)
        self.assertEqual(str(news_item_history), 'insert')

    def test_2_update(self):
        news_item = NewsItem.objects.create(title='My first news item',
                                            publish_date=datetime.datetime.now())

        news_item_count = NewsItem.objects.count()
        news_item_history_count = NewsItemHistory.objects.count()
        self.assertEqual(news_item_count, 1)
        self.assertEqual(news_item_history_count, 1)
        news_item = NewsItem.objects.get(pk=1)
        news_item.title = 'My first news item (updated)'
        news_item.save()

        news_item_count = NewsItem.objects.count()
        news_item_history_count = NewsItemHistory.objects.count()
        self.assertEqual(news_item_count, 1)
        self.assertEqual(news_item_history_count, 2)

        news_item = NewsItem.objects.get(pk=1)
        news_item_history = NewsItemHistory.objects.filter(history=news_item).order_by('pk')[1]
        self.assertEqual(news_item.title, news_item_history.title)
        self.assertEqual(news_item.description, news_item_history.description)
        self.assertEqual(news_item.publish_date, news_item_history.publish_date)
        self.assertEqual(str(news_item_history), 'update')

    def test_3_delete(self):
        news_item = NewsItem.objects.create(title='My first news item',
                                            publish_date=datetime.datetime.now())
        news_item_count = NewsItem.objects.count()
        news_item_history_count = NewsItemHistory.objects.count()
        self.assertEqual(news_item_count, 1)
        self.assertEqual(news_item_history_count, 1)
        news_item = NewsItem.objects.get(pk=1)
        news_item.delete()

        news_item_count = NewsItem.objects.count()
        news_item_history_count = NewsItemHistory.objects.count()

        news_item_history = NewsItemHistory.objects.get(pk=2)
        self.assertEqual(news_item_count, 0)
        self.assertEqual(news_item_history_count, 2)
        self.assertEqual(str(news_item_history), 'delete')