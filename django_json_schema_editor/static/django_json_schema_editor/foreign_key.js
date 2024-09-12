const { JSONEditor } = window

/* Patch functions with ones emitting a 'change' event after closing the popup */
document.addEventListener("DOMContentLoaded", () => {
  const __original_dismissRelatedLookupPopup = window.dismissRelatedLookupPopup
  window.dismissRelatedLookupPopup = (win, chosenId) => {
    // Django allows more than one popup per raw ID field, account for that.
    const input = document.getElementById(win.name.replace(/__[0-9]+$/, ""))
    __original_dismissRelatedLookupPopup(win, chosenId)

    input.dispatchEvent(new Event("input"))
  }
})
/* End patching */

JSONEditor.defaults.editors.foreign_key = class extends (
  JSONEditor.defaults.editors.string
) {
  build() {
    this.options.format = ""
    super.build()
    this.input_type = this.schema.format
  }

  afterInputReady() {
    const id = Math.random().toString(36).substr(2, 5)
    this.input.className = "vForeignKeyRawIdAdminField"
    this.input.setAttribute("id", `id_${id}`)
    this.input.setAttribute("name", id)

    this.input.addEventListener("input", (e) => {
      e.preventDefault()
      e.stopPropagation()

      this.value = this.input.value
      this.relatedName.textContent = ""
      this.onChange(true)
    })

    const relatedLookupLink = document.createElement("a")
    relatedLookupLink.className = "related-lookup"
    relatedLookupLink.setAttribute("id", `lookup_id_${id}`)
    relatedLookupLink.setAttribute("href", this.options.url)
    relatedLookupLink.setAttribute("title", "Nachschlagen")
    relatedLookupLink.setAttribute(
      "onclick",
      "return showRelatedObjectLookupPopup(this);",
    )

    this.relatedName = document.createElement("strong")
    this.relatedName.textContent =
      window.__djse_foreignKeys?.[`${this.options.model}:${this.value}`]

    const wrapper = document.createElement("div")
    wrapper.append(this.input, relatedLookupLink, this.relatedName)

    this.container.querySelector(".form-control").append(wrapper)
  }

  setValue(...args) {
    super.setValue(...args)
    if (this.relatedName) {
      this.relatedName.textContent =
        window.__djse_foreignKeys?.[`${this.options.model}:${this.value}`]
    }
  }
}

JSONEditor.defaults.resolvers.unshift((schema) => {
  if (schema.type === "string" && schema.format === "foreign_key") {
    return "foreign_key"
  }
})
