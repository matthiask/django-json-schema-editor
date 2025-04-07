import { createEditor } from "django-prose-editor/configurable"

function createJSONProseEditor(textarea, setClobber) {
  setClobber(null)
  createEditor(textarea, {
    extensions: {
      Document: true,
      Paragraph: true,
      HardBreak: true,
      Text: true,
      Bold: true,
      Italic: true,
      Underline: true,
      Subscript: true,
      Superscript: true,
      Menu: true,
    },
  }).then((editor) => {
    setClobber(() => {
      editor.destroy()
    })
  })
}

JSONEditor.defaults.editors.prose = class extends (
  JSONEditor.defaults.editors.string
) {
  setValue(value, initial, fromTemplate) {
    const res = super.setValue(value, initial, fromTemplate)

    if (res?.changed) {
      this.clobber?.()

      createJSONProseEditor(this.input, (clobber) => {
        this.clobber = clobber
      })
    }
  }

  build() {
    this.options.format = "textarea"
    super.build()
    this.input_type = this.schema.format // Restore original format
  }

  afterInputReady() {
    this.clobber?.()
    createJSONProseEditor(this.input, (clobber) => {
      this.clobber = clobber
    })

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
