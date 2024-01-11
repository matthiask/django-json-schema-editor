/* global JSONEditor */

JSONEditor.defaults.themes.django = class DjangoTheme extends (
  JSONEditor.AbstractTheme
) {
  getIndentedPanel() {
    let el = super.getIndentedPanel()

    // reset styles (borders/spacing)
    el.removeAttribute("style")

    // set class for easier styling via css
    el.setAttribute("class", "indented-panel")
    return el
  }
  getButton(text, icon, title) {
    let el = super.getButton(text, icon, title)
    el.setAttribute("class", `${el.getAttribute("class")} button`)
    return el
  }
  getButtonHolder() {
    let el = super.getButtonHolder()
    el.removeAttribute("style")
    el.classList.add("je-button-holder")
    return el
  }
  getHeaderButtonHolder() {
    let el = super.getHeaderButtonHolder()
    el.removeAttribute("style")
    el.classList.add("je-button-holder")
    return el
  }
  getTabHolder() {
    let el = super.getTabHolder()
    el.setAttribute("class", "je-tab-holder")
    el.innerHTML = [
      "<div class='je-tabs'></div>",
      "<div class='je-content'></div>",
      "<div style='clear:both;'></div>",
    ].join("")
    return el
  }
  getTab(span) {
    let el = super.getTab(span)
    el.appendChild(span)
    el.setAttribute("class", "je-tab button")
    el.removeAttribute("style")
    return el
  }
  markTabActive(row) {
    super.markTabActive(row)
    row.tab.classList.add("active")
    row.tab.removeAttribute("style")
  }
  getTextareaInput() {
    // reset styles
    let el = super.getTextareaInput()

    // set class for easier styling via css
    el.removeAttribute("style")
    return el
  }
  setGridColumnSize(el, size) {
    el.setAttribute("style", `width: ${(size / 12) * 100}%`)
  }
}
