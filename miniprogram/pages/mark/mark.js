Page({
  data: {
    groupId: '',
    messageText: '',
    messageTime: '',
    reason: '无关信息',
    suggestKick: false,
    marking: false,
    marked: false,
    reasons: ['无关信息', '不当言论', '言语冲突', '其他'],
  },

  onLoad(options) {
    // 从分享链接或扫描二维码进入，带群ID和消息内容
    if (options.groupId) this.setData({ groupId: options.groupId })
    if (options.messageText) this.setData({ messageText: options.messageText })
    if (options.messageTime) this.setData({ messageTime: options.messageTime })
  },

  onReasonChange(e) {
    this.setData({ reason: e.detail.value })
  },

  toggleKick() {
    this.setData({ suggestKick: !this.data.suggestKick })
  },

  async onSubmit() {
    const { groupId, messageText, messageTime, reason, suggestKick } = this.data
    if (!messageText.trim()) {
      wx.showToast({ title: '请填写消息内容', icon: 'none' })
      return
    }
    this.setData({ marking: true })
    try {
      const token = wx.getStorageSync('token')
      const resp = await fetch('https://your-api-host/api/marks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          group_id: groupId,
          message_text: messageText,
          message_time: messageTime || new Date().toISOString(),
          reason,
          suggest_kick: suggestKick,
        }),
      })
      if (resp.ok) {
        this.setData({ marked: true, messageText: '' })
        wx.showToast({ title: '标记成功' })
      } else {
        wx.showToast({ title: '标记失败', icon: 'none' })
      }
    } catch (err) {
      console.error(err)
      wx.showToast({ title: '网络错误', icon: 'none' })
    } finally {
      this.setData({ marking: false })
    }
  },
})
