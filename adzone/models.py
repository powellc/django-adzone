# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from adzone.managers import AdManager

class Advertiser(models.Model):
    """ A Model for our Advertiser
    """
    company_name = models.CharField(max_length=255)
    website = models.URLField(verify_exists=False)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return "%s" % self.company_name

    def get_website_url(self):
        return "%s" % self.website

class AdCategory(models.Model):
    """
    a Model to hold the different Categories for adverts

    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = 'Ad Category'
        verbose_name_plural = 'Ad Categories'

    def __unicode__(self):
        return "%s" % self.title

class AdZone(models.Model):
    """
    a Model that describes the attributes and behaviours of ad zones

    """
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()

    class Meta:
        verbose_name = 'Ad Zone'
        verbose_name_plural = 'Ad Zones'

    def __unicode__(self):
        return "%s" % self.title

class AdBase(models.Model):
    """
    This is our base model, from which all ads will inherit.
    The manager methods for this model will determine which ads to
    display return etc.

    """
    title = models.CharField(max_length=255)
    url = models.URLField(verify_exists=False)
    enabled = models.BooleanField(default=False)
    since = models.DateTimeField(default=datetime.now)
    expires_on=models.DateTimeField(_('Expires on'), blank=True, null=True)
    updated = models.DateTimeField(editable=False, auto_now=True)

    # Relations
    advertiser = models.ForeignKey(Advertiser)
    category = models.ForeignKey(AdCategory)
    zone = models.ForeignKey(AdZone)

    # Our Custom Manager
    objects = AdManager()

    def __unicode__(self):
        return "%s" % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('adzone_ad_view', [self.id])

    def impressions(self, start=None, end=None):
        if start is not None:
            start_q=models.Q(impression_date__gte=start)
        else:
            start_q=models.Q()
        if end is not None:
            end_q=models.Q(impression_date__lte=end)
        else:
            end_q=models.Q()
        return self.adimpression_set.filter(start_q & end_q).count()

    def clicks(self, start=None, end=None):
        if start is not None:
            start_q=models.Q(click_date__gte=start)
        else:
            start_q=models.Q()
        if end is not None:
            end_q=models.Q(click_date__lte=end)
        else:
            end_q=models.Q()
        return self.adclick_set.filter(start_q & end_q).count()

class AdImpression(models.Model):
    """
    The AdImpression Model will record every time the ad is loaded on a page

    """
    impression_date = models.DateTimeField(default=datetime.now)
    source_ip = models.IPAddressField(null=True, blank=True)
    ad = models.ForeignKey(AdBase)

    class Meta:
        verbose_name = 'Ad Impression'
        verbose_name_plural = 'Ad Impressions'

class AdClick(models.Model):
    """
    The AdClick model will record every click that a add gets

    """
    click_date = models.DateTimeField(default=datetime.now)
    source_ip = models.IPAddressField(null=True, blank=True)
    ad = models.ForeignKey(AdBase)

    class Meta:
        verbose_name = 'Ad Click'
        verbose_name_plural = 'Ad Clicks'

# Example Ad Types
class TextAd(AdBase):
    """ A most basic, text based advert """
    content = models.TextField()

class BannerAd(AdBase):
    """ A standard banner Ad """
    content = models.ImageField(upload_to="zone/banners/")
