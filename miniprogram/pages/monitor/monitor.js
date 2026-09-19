Page({
  data: {
    groupId: 'default_group',
    messageText: '',
    messages: [],
    loading: false,
    refreshing: false,
    autoAnalyze: true,      // 是否自动AI分析
  },

  onShow() {
    this.loadMessages()
  },

  async loadMessages() {
    this.setData({ loading: true })
    try {
      const token = wx.getStorageSync('token')
      const resp = await fetch(
        `https://your-api-host/api/monitor/list?group_id=${this.data.groupId}&limit=50`,
        { headers: { Authorization: `Bearer ${token}` } }
      )
      const data = await resp.json()
      if (resp.ok) {
        this.setData({ messages: data.data || [] })
      }
    } catch (err) {
      console.error(err)
    } finally {
      this.setData({ loading: false, refreshing: false })
    }
  },

  onMessageInput(e) {
    this.setData({ messageText: e.detail.value })
  },

  // 手动添加消息 → AI自动分析
  async onAddMessage() {
    const { messageText, groupId } = this.data
    if (!messageText.trim()) {
      wx.showToast({ title: '请输入消息内容', icon: 'none' })
      return
    }
    this.setData({ loading: true })
    try {
      const token = wx.getStorageSync('token')
      const resp = await fetch('https://your-api-host/api/monitor', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          group_id: groupId,
          message_text: messageText.trim(),
          sender: '未知用户',
        }),
      })
      const data = await resp.json()
      if (resp.ok) {
        wx.showToast({ title: data.data.is_abnormal ? '⚠️ 检测到异常' : '✓ 正常消息' })
        this.setData({ messageText: '' })
        this.loadMessages()
      } else {
        wx.showToast({ title: data.msg || '添加失败', icon: 'none' })
      }
    } catch (err) {
      console.error(err)
      wx.showToast({ title: '网络错误', icon: 'none' })
    } finally {
      this.setData({ loading: false })
    }
  },

  // 确认异常
  async onConfirm(e) {
    const id = e.currentTarget.dataset.id
    const token = wx.getStorageSync('token')
    try {
      const resp = await fetch(`https://your-api-host/api/monitor/${id}/confirm`, {
        method: 'PUT',
        headers: { Authorization: `Bearer ${token}` },
      })
      if (resp.ok) {
        wx.showToast({ title: '已确认' })
        this.loadMessages()
      }
    } catch (err) {
      console.error(err)
    }
  },

  // 驳回误判
  async onReject(e) {
    const id = e.currentTarget.dataset.id
    const token = wx.getStorageSync('token')
    try {
      const resp = await fetch(`https://your-api-host/api/monitor/${id}/reject`, {
        method: 'PUT',
        headers: { Authorization: `Bearer ${token}` },
      })
      if (resp.ok) {
        wx.showToast({ title: '已驳回' })
        this.loadMessages()
      }
    } catch (err) {
      console.error(err)
    }
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.setData({ refreshing: true })
    this.loadMessages()
  },
})
