from django.db import models
from jsonfield import JSONField


class KqJsons(models.Model):
    nid = models.CharField(
        max_length=36
    )
    sid = models.CharField(
        max_length=36
    )
    cid = models.CharField(
        max_length=36
    )
    json = JSONField()
    seq_id = models.IntegerField()
    time_stamp = models.DateTimeField()

    def __str__(self):
        return '%s %s %s %s' % (self.sid, self.nid, self.cid, self.seq_id)

    class Meta:
        ordering = ('-time_stamp',)
        verbose_name = 'kqjson'
        verbose_name_plural = 'kqjsons'

class ScaffoldJsons(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=36
    )
    sid = models.CharField(
        max_length=36
    )
    
    json = JSONField()

    def __str__(self):
        return '%s %s' % (self.id, self.sid)

    class Meta:
        verbose_name = 'scaffoldjson'
        verbose_name_plural = 'scaffoldjsons'


class SessionDetails(models.Model):
    sid = models.CharField(
        max_length=36
    )
    cid = models.CharField(
        max_length=36
    )
    notebook_cid = models.CharField(
        max_length=12
    )
    cid_hash = models.CharField(
        max_length=36
    )
    code_id = models.IntegerField()
    source = models.TextField()
    output = models.TextField()
    code_eval = models.IntegerField()
    time_stamp = models.DateTimeField()

    def __str__(self):
        return '%s %s %s %s' % (self.sid, self.cid, self.notebook_cid, self.code_id)

    class Meta:
        ordering = ('-time_stamp',)
        verbose_name = 'session_detail'
        verbose_name_plural = 'session_details'


class KqClone(models.Model):
    sid = models.CharField(
        max_length=36
    )
    cid = models.CharField(
        max_length=36
    )
    result = models.TextField()
    valid = models.IntegerField()
    eval_score = models.IntegerField()
    count = models.IntegerField()
    time_stamp = models.DateTimeField()

    def __str__(self):
        return '%s %s' % (self.sid, self.cid)

    class Meta:
        ordering = ('-time_stamp',)
        verbose_name = 'kqclone'
        verbose_name_plural = 'kqclones'


class GDTemplateTracker(models.Model):
    gid = models.CharField(
        max_length=36
    )
    sid = models.CharField(
        max_length=36
    )
    nid = models.CharField(
        max_length=36
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return '%s %s %s' % (self.sid, self.gid, self.nid)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'gd_template_tracker'
        verbose_name_plural = 'gd_template_trackers'
