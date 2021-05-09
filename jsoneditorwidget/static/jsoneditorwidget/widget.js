document.addEventListener("DOMContentLoaded", event => {
  document.querySelectorAll(".inline-related:not(.empty-form) .jsoneditorwidget").forEach(el => {
    DjangoJSONEditorWidget.initWidget(el);
  });
})

document.addEventListener("DOMContentLoaded", event => {
  django.jQuery(document).on("formset:added", (event, $row, formsetName) => {
    $row.get().forEach(el => {
      el.querySelectorAll(".jsoneditorwidget").forEach(
        el => DjangoJSONEditorWidget.initWidget(el)
      )
    });
  });
})

const DjangoJSONEditorWidget = {
  initWidget: (el) => {
    DjangoJSONEditorWidget.initEditor(el);
    DjangoJSONEditorWidget.initDatafieldToggle(el);
  },
  initEditor: (el) => {
    const container = el.querySelector(".editor")
    const input = el.querySelector("textarea")
    const config = JSON.parse(el.dataset["editorConfig"])
    const editor = new JSONEditor(container, config);

    const data = JSON.parse(input.value);
    if (data) {
      editor.setValue({...editor.getValue(), ...data})
    }

    editor.on('change', e => {
      input.value = JSON.stringify(editor.getValue());
    });
  },
  initDatafieldToggle: (el) => {
    const toggle = el.querySelector('.datafield-toggle');
    const showText = toggle.dataset["showText"];
    const hideText = toggle.dataset["hideText"];
    const wrapper = el.querySelector(".datafield-wrapper");

    toggle.text = showText;
    wrapper.classList.add("hidden")

    toggle.addEventListener("click", e => {
      e.preventDefault();

      if (wrapper.classList.contains("hidden")) {
        // show
        wrapper.classList.remove("hidden");
        toggle.text = hideText;
      } else {
        // hide
        wrapper.classList.add("hidden");
        toggle.text = showText;
      }
    })
  }
}
