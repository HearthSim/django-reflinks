from uuid import uuid4

from django.conf import settings
from django.db import models
from django.urls import reverse


class ReferralHitManager(models.Manager):
	pass


class ReferralLink(models.Model):
	id = models.AutoField(primary_key=True, serialize=False, verbose_name="ID")
	identifier = models.CharField(max_length=50, blank=True, unique=True)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
	)
	disabled = models.BooleanField(default=False)

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.get_absolute_url()

	def get_absolute_url(self):
		return reverse("django_reflinks_reflink", kwargs={"identifier": self.identifier})


class ReferralHit(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	referral_link = models.ForeignKey(ReferralLink, on_delete=models.CASCADE)
	authenticated = models.BooleanField(
		help_text="Whether the hit was created by an authenticated user."
	)
	hit_user = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
	)
	ip = models.GenericIPAddressField(help_text="IP address at hit time")
	user_agent = models.TextField(blank=True, help_text="User-Agent at hit time")
	http_referer = models.TextField(blank=True, help_text="Referer header at hit time")
	next = models.URLField(blank=True, help_text="The ?next parameter when the link was hit.")
	confirmed = models.DateTimeField(
		null=True, blank=True, db_index=True,
		help_text="If set, the datetime at which the hit was marked as a successful referral."
	)

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.hit_user or '(anonymous user)'} -> {self.referral_link}"
