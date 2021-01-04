<template>
  <div />
</template>
<script>
import plupload from 'plupload'
export default {
  name: 'Uploader',
  props: {
    browseButton: {
      type: String,
      default: ''
    },
    container: {
      type: String,
      default: ''
    },
    url: {
      type: String,
      default: ''
    },
    filters: {
      type: Object,
      default: null
    },
    headers: {
      type: Object,
      default: null
    },
    multipartParams: {
      type: Object,
      default: null
    },
    resize: {
      type: Object,
      default: null
    },
    dropElement: {
      type: String,
      default: ''
    },
    requiredFeatures: {
      type: String,
      default: ''
    },
    runtimes: {
      type: String,
      default() {
        return 'html5,flash,silverlight,html4'
      }
    },
    chunkSize: {
      type: String,
      default() {
        return '0'
      }
    },
    multipart: {
      type: Boolean,
      default() {
        return true
      }
    },
    maxRetries: {
      type: Number,
      default() {
        return 0
      }
    },
    multiSelection: {
      type: Boolean,
      default() {
        return true
      }
    },
    uniqueNames: {
      type: Boolean,
      default() {
        return false
      }
    },
    fileDataName: {
      type: String,
      default() {
        return 'file'
      }
    },
    flashSwfUrl: {
      type: String,
      default() {
        return 'plupload/js/Moxie.swf'
      }
    },
    silverlightXapUrl: {
      type: String,
      default() {
        return 'plupload/js/Moxie.xap'
      }
    }
    // init: {
    //   type: Function
    // },
    // postInit: {
    //   type: Function
    // },
    // browse: {
    //   type: Function
    // },
    // optionChanged: {
    //   type: Function
    // },
    // refresh: {
    //   type: Function
    // },
    // stateChanged: {
    //   type: Function
    // },
    // uploadFile: {
    //   type: Function
    // },
    // beforeUpload: {
    //   type: Function
    // },
    // queueChanged: {
    //   type: Function
    // },
    // uploadProgress: {
    //   type: Function
    // },
    // filesRemoved: {
    //   type: Function
    // },
    // fileFiltered: {
    //   type: Function
    // },
    // filesAdded: {
    //   type: Function
    // },
    // fileUploaded: {
    //   type: Function
    // },
    // chunkUploaded: {
    //   type: Function
    // },
    // uploadComplete: {
    //   type: Function
    // },
    // error: {
    //   type: Function
    // },
    // destroy: {
    //   type: Function
    // }
  },
  data() {
    return {
      up: {}
    }
  },
  watch: {
    up(val) {
      this.$emit('inputUploader', val)
    }
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      const that = this
      const preInitMethod = {
        Init(up, info) {
          if (that.Init != null) {
            that.Init(up, info)
          }
        },
        UploadFile(up, file) {
          if (that.UploadFile != null) {
            that.UploadFile(up, file)
          }
        }
      }
      const initMethod = {
        PostInit() {
          if (that.PostInit != null) {
            that.PostInit()
          }
        },
        Browse(up) {
          if (that.Browse != null) {
            that.Browse(up)
          }
        },
        OptionChanged(up, name, value, oldValue) {
          if (that.OptionChanged != null) {
            that.OptionChanged(up, name, value, oldValue)
          }
        },
        Refresh(up) {
          if (that.Refresh != null) {
            that.Refresh(up)
          }
        },
        StateChanged(up) {
          if (that.StateChanged != null) {
            that.StateChanged(up)
          }
        },
        BeforeUpload(up, file) {
          if (that.BeforeUpload != null) {
            that.BeforeUpload(up, file)
          }
        },
        QueueChanged(up) {
          if (that.QueueChanged != null) {
            that.QueueChanged(up)
          }
        },
        UploadProgress(up, file) {
          if (that.UploadProgress != null) {
            that.UploadProgress(up, file)
          }
        },
        FilesRemoved(up, files) {
          if (that.FilesRemoved != null) {
            that.FilesRemoved(up, files)
          }
        },
        FileFiltered(up, file) {
          if (that.FileFiltered != null) {
            that.FileFiltered(up, file)
          }
        },
        FilesAdded(up, files) {
          if (that.FilesAdded != null) {
            that.FilesAdded(up, files)
          }
        },
        FileUploaded(up, file, info) {
          if (that.FileUploaded != null) {
            that.FileUploaded(up, file, info)
          }
        },
        ChunkUploaded(up, file, info) {
          if (that.ChunkUploaded != null) {
            that.ChunkUploaded(up, file, info)
          }
        },
        UploadComplete(up, files) {
          if (that.UploadComplete != null) {
            that.UploadComplete(up, files)
          }
        },
        Error(up, args) {
          if (that.Error != null) {
            that.Error(up, args)
          }
        },
        Destroy(up) {
          if (that.Destroy != null) {
            that.Destroy(up)
          }
        }
      }
      const prop = {
        runtimes: this.runtimes,
        browse_button: this.browse_button,
        container: this.container,
        url: this.url,
        chunk_size: this.chunk_size,
        headers: this.headers,
        multipart: this.multipart,
        max_retries: this.max_retries,
        multi_selection: this.multi_selection,
        unique_names: this.unique_names,
        file_data_name: this.file_data_name,
        flash_swf_url: this.flash_swf_url,
        silverlight_xap_url: this.silverlight_xap_url,
        preinit: preInitMethod,
        init: initMethod
      }
      if (this.filters != null) {
        prop['filters'] = this.filters
      }
      if (this.multipart_params != null) {
        prop['multipart_params'] = this.multipart_params
      }
      if (this.resize != null) {
        prop['resize'] = this.resize
      }
      if (this.drop_element != null) {
        prop['drop_element'] = this.drop_element
      }
      if (this.required_features != null) {
        prop['required_features'] = this.required_features
      }
      const uploader = new plupload.Uploader(prop)
      uploader.init()
      this.up = uploader
    }
  }
}
</script>
