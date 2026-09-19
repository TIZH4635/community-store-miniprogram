Page({
  data: {
    pushTimes: ['07:15', '11:30', '17:30', '20:30'],
    saving: false,
    saved: false,
  },

  onShow() {
    this.loadSettings()
  },

  async loadSettings() {
    try {
      const token = wx.getStorageSync('token')
      const resp = await fetch('https://your-api-host/api/settings/push_times', {
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await resp.json()
      if (resp.ok && data.data) {
        this.setData({ pushTimes: data.data.value })
      }
    } catch (err) {
      console.error(err)
    }
  },

  onTimeChange(e) {
    const idx = e.currentTarget.dataset.index
    const times = [...this.data.pushTimes]
    times[idx] = e.detail.value
    this.setData({ pushTimes: times, saved: false })
  },

  async onSave() {
    this.setData({ saving: true })
    try {
      const token = wx.getStorageSync('token')
      const resp = await fetch('https://your-api-host/api/settings/push_times', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ value: this.data.pushTimes }),
      })
      if (resp.ok) {
        this.setData({ saved: true })
        wx.showToast({ title: '保存成功' })
      } else {
        wx.showToast({ title: '保存失败', icon: 'none' })
      }
    } catch (err) {
      console.error(err)
      wx.showToast({ title: '网络错误', icon: 'none' })
    } finally {
      this.setData({ saving: false })
    }
  },
})
