Page({
  data: {
    userInfo: null,
    role: null,
  },

  onShow() {
    const userInfo = wx.getStorageSync('userInfo')
    const role = wx.getStorageSync('role')
    console.log('index onShow:', { userInfo, role })
    this.setData({ userInfo, role })
    this.checkReminders()
  },

  checkReminders() {
    // 检查当前时间是否在推送时间窗口内
    const now = new Date()
    const hh = String(now.getHours()).padStart(2, '0')
    const mm = String(now.getMinutes()).padStart(2, '0')
    const currentTime = `${hh}:${mm}`
    const pushTimes = ['07:15', '11:30', '17:30', '20:30']
    if (pushTimes.includes(currentTime)) {
      wx.showToast({ title: '该发布商品了', icon: 'none' })
    }
  },

  onLoad() {
    console.log('index onLoad')
  },

  onLogout() {
    wx.removeStorageSync('token')
    wx.removeStorageSync('userInfo')
    wx.removeStorageSync('role')
    wx.switchTab({ url: '/pages/login/login' })
  },

  navigateToPublish() {
    wx.navigateTo({ url: '/pages/publish/publish' })
  },

  navigateToPush() {
    wx.navigateTo({ url: '/pages/push/push' })
  },

  navigateToMark() {
    wx.navigateTo({ url: '/pages/mark/mark' })
  },

  navigateToMarks() {
    wx.navigateTo({ url: '/pages/marks/marks' })
  },

  navigateToAI() {
    wx.navigateTo({ url: '/pages/ai/ai' })
  },

  navigateToMonitor() {
    wx.navigateTo({ url: '/pages/monitor/monitor' })
  },
})