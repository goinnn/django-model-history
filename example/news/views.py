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


from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _


def auto_login(request):
    user, created = User.objects.get_or_create(username='model_history_admin',
                                               is_staff=True,
                                               is_superuser=True)
    if not hasattr(user, 'backend'):
        user.backend = settings.AUTHENTICATION_BACKENDS[0]
    login(request, user)
    messages.info(request, _('E.g.: Add/update or delete news, and after it browse to `News item change histories`'))
    return HttpResponseRedirect(reverse('admin:app_list', args=('news',)))