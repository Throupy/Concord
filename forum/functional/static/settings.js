$(function() {
  $('#darkThemeToggle').change(function() {
    if (Cookies.get('darkTheme') == 'true') {
      Cookies.set('darkTheme', false)
    } else {
      Cookies.set('darkTheme', true)
    }
    location.reload()
  })
})
