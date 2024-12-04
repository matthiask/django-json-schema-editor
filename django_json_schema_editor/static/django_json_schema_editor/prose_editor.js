function createJSONProseEditor(textarea) {
  const {
    // Always recommended:
    Document,
    Dropcursor,
    Gapcursor,
    Paragraph,
    HardBreak,
    Text,

    // Add support for a few marks:
    Bold,
    Italic,
    Underline,
    Subscript,
    Superscript,

    // A menu is always nice:
    Menu,

    // Useful:
    createTextareaEditor,
  } = window.DjangoProseEditor

  const extensions = [
    Document,
    Dropcursor,
    Gapcursor,
    Paragraph,
    HardBreak,
    Text,
    Bold,
    Italic,
    Underline,
    Subscript,
    Superscript,
    Menu,
  ]

  const editor = createTextareaEditor(textarea, extensions)
  return () => {
    editor.destroy()
  }
}

JSONEditor.defaults.editors.prose = class extends (
  JSONEditor.defaults.editors.string
) {
  setValue(value, initial, fromTemplate) {
    const res = super.setValue(value, initial, fromTemplate)

    if (res?.changed) {
      this.clobber?.()
      this.clobber = createJSONProseEditor(this.input)
    }
  }

  build() {
    this.options.format = "textarea"
    super.build()
    this.input_type = this.schema.format // Restore original format
  }

  afterInputReady() {
    this.clobber?.()
    this.clobber = createJSONProseEditor(this.input)

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
