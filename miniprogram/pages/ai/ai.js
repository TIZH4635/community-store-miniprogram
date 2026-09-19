Page({
  data: {
    messageText: '',
    loading: false,
    result: null,
    keywords: [],
  },

  onShow() {
    this.loadKeywords()
  },

  async loadKeywords() {
    try {
      const token = wx.getStorageSync('token')
      const resp = await fetch('https://your-api-host/api/ai/keywords', {
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await resp.json()
      if (resp.ok) {
        this.setData({ keywords: data.data || [] })
      }
    } catch (err) {
      console.error(err)
    }
  },

  onMessageInput(e) {
    this.setData({ messageText: e.detail.value })
  },

  async onAnalyze() {
    const { messageText, keywords } = this.data
    if (!messageText.trim()) {
      wx.showToast({ title: '请粘贴消息内容', icon: 'none' })
      return
    }
    this.setData({ loading: true })
    try {
      const token = wx.getStorageSync('token')
      const resp = await fetch('https://your-api-host/api/ai/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ message_text: messageText.trim(), keywords }),
      })
      const data = await resp.json()
      if (resp.ok) {
        this.setData({ result: data.data })
      } else {
        wx.showToast({ title: data.msg || '分析失败', icon: 'none' })
      }
    } catch (err) {
      console.error(err)
      wx.showToast({ title: '网络错误', icon: 'none' })
    } finally {
      this.setData({ loading: false })
    }
  },

  async onConfirm() {
    const { result, messageText } = this.data
    if (!result) return
    this.setData({ loading: true })
    try {
      const token = wx.getStorageSync('token')
      // 创建标记
      const markResp = await fetch('https://your-api-host/api/marks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          group_id: '',
          message_text: messageText,
          message_time: new Date().toISOString(),
          reason: result.reason,
          suggest_kick: false,
        }),
      })
      // 新增敏感词
      if (result.suggested_keywords && result.suggested_keywords.length > 0) {
        await fetch('https://your-api-host/api/ai/keywords', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ words: result.suggested_keywords }),
        })
      }
      if (markResp.ok) {
        wx.showToast({ title: '已标记 + 敏感词已更新' })
        this.setData({ messageText: '', result: null })
      }
    } catch (err) {
      console.error(err)
      wx.showToast({ title: '操作失败', icon: 'none' })
    } finally {
      this.setData({ loading: false })
    }
  },
})
