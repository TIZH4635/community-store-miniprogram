Page({
  data: {
    loading: false,
  },

  onLoad() {},

  async onGetUserInfo(e) {
    if (!e.detail.userInfo) {
      wx.showToast({ title: '需授权登录', icon: 'none' })
      return
    }
    this.setData({ loading: true })
    try {
      const loginRes = await wx.login()
      console.log('wx.login code:', loginRes.code)
      const userInfo = e.detail.userInfo
      console.log('userInfo:', userInfo)
      wx.setStorageSync('token', 'mock-token')
      wx.setStorageSync('userInfo', userInfo)
      wx.setStorageSync('role', 'store_admin')
      console.log('storage set, reLaunching...')
      wx.reLaunch({ url: '/pages/index/index' })
    } catch (err) {
      console.error('login error:', err)
      wx.showToast({ title: '登录失败', icon: 'none' })
    } finally {
      this.setData({ loading: false })
    }
  },
})