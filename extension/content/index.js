
var jcrop, selection

var config = {
  method: 'crop',
  format: 'png',
  quality: 100,
  scaling: true,
  save: ['file'],
  clipboard: 'url',
  dialog: true,
  icon: 'default',
}

var overlay = ((active) => (state) => {
  active = typeof state === 'boolean' ? state : state === null ? active : !active
  $('.jcrop-holder')[active ? 'show' : 'hide']()
  chrome.runtime.sendMessage({ message: 'active', active })
})(false)

var image = (done) => {
  var image = new Image()
  image.id = 'fake-image'
  image.src = chrome.runtime.getURL('/content/pixel.png')
  image.onload = () => {
    $('body').append(image)
    done()
  }
}

var init = (done) => {
  $('#fake-image').Jcrop({
    bgColor: 'none',
    onSelect: (e) => {
      selection = e
      capture()
    },
    onChange: (e) => {
      selection = e
    },
    onRelease: (e) => {
      setTimeout(() => {
        selection = null
      }, 100)
    }
  }, function ready() {
    jcrop = this

    $('.jcrop-hline, .jcrop-vline').css({
      backgroundImage: `url(${chrome.runtime.getURL('/vendor/Jcrop.gif')})`
    })

    if (selection) {
      jcrop.setSelect([
        selection.x, selection.y,
        selection.x2, selection.y2
      ])
    }

    done && done()
  })
}

var capture = (force) => {
  if (selection && (config.method === 'crop' || (config.method === 'wait' && force))) {
    jcrop.release()
    setTimeout(() => {
      var _selection = selection
      chrome.runtime.sendMessage({
        message: 'capture', format: config.format, quality: config.quality
      }, (res) => {
        overlay(false)
        crop(res.image, _selection, devicePixelRatio, config.scaling, config.format, (image) => {
          sendToBackground(image, true)
          selection = null
        })
      })
    }, 50)
  } else if (config.method === 'page') {
    chrome.runtime.sendMessage({
      message: 'capture', format: config.format, quality: config.quality
    }, (res) => {
      overlay(false)
      if (devicePixelRatio !== 1 && !config.scaling) {
        var area = { x: 0, y: 0, w: innerWidth, h: innerHeight }
        crop(res.image, area, devicePixelRatio, config.scaling, config.format, (image) => {
          sendToBackground(image, false)
        })
      }
      else {
        sendToBackground(res.image, false)
      }
    })
  }
}

var sendToBackground = (image, open) => {
  data = {image , open}
  setTimeout(()=>{
    chrome.runtime.sendMessage({ message: 'returnImage', data }, (response) => {
      if (chrome.runtime.lastError) {
        console.error("Error sending message:", chrome.runtime.lastError);
      }
    });
  }, 50)
};

window.addEventListener('resize', ((timeout) => () => {
  clearTimeout(timeout)
  timeout = setTimeout(() => {
    jcrop.destroy()
    init(() => overlay(null))
  }, 100)
})())

chrome.runtime.onMessage.addListener((req, sender, res) => {
  config.method = req.method
  if (req.message === 'init') {
    res({}) // prevent re-injecting

    if (!jcrop) {
      image(() => init(() => {
        overlay()
        capture()
      }))
    }
    else {
      overlay()
      capture(true)
    }
  }
  return true
})
