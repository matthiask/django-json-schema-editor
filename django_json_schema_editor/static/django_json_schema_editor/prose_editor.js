const config = {
  // Hardcoded for now.
  types: ["hard_break", "strong", "em", "underline", "sub", "sup"],
}

JSONEditor.defaults.editors.prose = class extends (
  JSONEditor.defaults.editors.string
) {
  setValue(value, initial, fromTemplate) {
    const res = super.setValue(value, initial, fromTemplate)

    if (res?.changed) {
      this.clobber?.()
      this.clobber = DjangoProseEditor.createEditor(this.input, config)
    }
  }

  build() {
    this.options.format = "textarea"
    super.build()
    this.input_type = this.schema.format // Restore original format
  }

  afterInputReady() {
    this.clobber?.()
    this.clobber = DjangoProseEditor.createEditor(this.input, config)

    this.input.addEventListener("input", (e) => {
      e.preventDefault()
      e.stopPropagation()

      this.value = this.input.value
      this.onChange(true)
    })
  }

  getNumColumns() {
    return 6
  }
}

JSONEditor.defaults.resolvers.unshift((schema) => {
  if (schema.type === "string" && schema.format === "prose") {
    return "prose"
  }
})
