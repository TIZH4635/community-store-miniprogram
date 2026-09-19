Page({
  data: {
    title: '',
    description: '',
    photos: [],
    maxPhotos: 5,
    publishing: false,
    previewVisible: false,
  },

  onLoad() {
    // 启用分享菜单
    wx.showShareMenu({ withShareTicket: true })
  },

  // --- 输入 ---
  onTitleInput(e) {
    this.setData({ title: e.detail.value })
  },
  onDescriptionInput(e) {
    this.setData({ description: e.detail.value })
  },

  // --- 照片选择 ---
  async choosePhoto() {
    const { photos, maxPhotos } = this.data
    const remain = maxPhotos - photos.length
    if (remain <= 0) {
      wx.showToast({ title: `最多${maxPhotos}张`, icon: 'none' })
      return
    }
    try {
      const res = await wx.chooseMedia({
        count: remain,
        sizeType: ['compressed'],
        sourceType: ['album', 'camera'],
        mediaType: ['image'],
      })
      const tempPaths = res.tempFiles.map(f => f.tempFilePath)
      const compressed = await this._checkAndCompress(tempPaths)
      this.setData({ photos: [...this.data.photos, ...compressed] })
    } catch (err) {
      console.error('choosePhoto error', err)
    }
  },

  // 预览照片
  previewPhoto(e) {
    const idx = e.currentTarget.dataset.index
    wx.previewImage({ current: this.data.photos[idx], urls: this.data.photos })
  },

  // 删除照片
  removePhoto(e) {
    const idx = e.currentTarget.dataset.index
    this.setData({ photos: this.data.photos.filter((_, i) => i !== idx) })
  },

  // --- 压缩逻辑 ---
  async _checkAndCompress(paths) {
    const result = []
    for (const path of paths) {
      const info = await wx.getFileInfo({ filePath: path })
      if (info.size > 3 * 1024 * 1024) {
        const compressed = await wx.compressImage({
          src: path,
          quality: 60,
        })
        result.push(compressed.tempFilePath)
      } else {
        result.push(path)
      }
    }
    return result
  },

  // --- 预览分享卡片 ---
  onPreview() {
    const { title, photos } = this.data
    if (!title.trim()) { wx.showToast({ title: '请输入标题', icon: 'none' }); return }
    if (photos.length < 2) { wx.showToast({ title: '至少2张照片', icon: 'none' }); return }
    this.setData({ previewVisible: true })
  },

  // --- 微信分享配置 ---
  onShareAppMessage() {
    const { title, description, photos } = this.data
    return {
      title: title.trim() || '社区商店商品信息',
      desc: description.trim() || '社区商店商品信息',
      imgUrl: photos[0] || '',
      path: '/pages/publish/publish',
    }
  },

  // --- 重置 ---
  onReset() {
    this.setData({ title: '', description: '', photos: [], previewVisible: false })
  },

  // --- 关闭预览 ---
  onClosePreview() {
    this.setData({ previewVisible: false })
  },
})
