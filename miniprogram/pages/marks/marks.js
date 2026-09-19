Page({
  data: {
    marks: [],
    loading: false,
    filter: 'all', // all / pending
  },

  onShow() {
    this.loadMarks()
  },

  async loadMarks() {
    this.setData({ loading: true })
    try {
      const token = wx.getStorageSync('token')
      const url = this.data.filter === 'pending'
        ? 'https://your-api-host/api/marks/pending'
        : 'https://your-api-host/api/marks/all'
      const resp = await fetch(url, {
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await resp.json()
      if (resp.ok) {
        this.setData({ marks: data.data || [] })
      }
    } catch (err) {
      console.error(err)
    } finally {
      this.setData({ loading: false })
    }
  },

  onFilterChange(e) {
    this.setData({ filter: e.detail.value }, () => this.loadMarks())
  },

  async onResolve(e) {
    const id = e.currentTarget.dataset.id
    const token = wx.getStorageSync('token')
    try {
      const resp = await fetch(`https://your-api-host/api/marks/${id}/resolve`, {
        method: 'PUT',
        headers: { Authorization: `Bearer ${token}` },
      })
      if (resp.ok) {
        wx.showToast({ title: '已处理' })
        this.loadMarks()
      }
    } catch (err) {
      console.error(err)
    }
  },
})
