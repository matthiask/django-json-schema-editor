/* global JSONEditor */
JSONEditor.defaults.language = "de"
JSONEditor.defaults.languages.de = {
  error_notset: "Eigenschaft muss gesetzt sein",
  error_notempty: "Wert wird benötigt",
  error_enum: "Wert muss einer der erlaubten Werte sein",
  error_const: "Wert muss der konstante Wert sein",
  error_anyOf:
    "Wert muss mit mindestens einem der bereitgestellten Schemas entsprechen",
  error_oneOf:
    "Wert muss genau einem der bereitgestellten Schemas enstprechen. Aktuell entspricht er {{0}} der Schemas.",
  error_not: "Wert darf dem bereitgestelltem Schema nicht entsprechen",
  error_type_union: "Wert muss einen der bereitgestellten Typen haben",
  error_type: "Wert muss vom Typ {{0}} sein",
  error_disallow_union:
    "Wert darf nicht von einem der bereitgestellten verbotenen Typen sein",
  error_disallow: "Wert darf nicht vom Typ {{0}} sein",
  error_multipleOf: "Wert muss ein Vielfaches von {{0}} sein",
  error_maximum_excl: "Wert muss weniger als {{0}} sein",
  error_maximum_incl: "Wert muss höchstens {{0}} sein",
  error_minimum_excl: "Wert muss grösser als {{0}} sein",
  error_minimum_incl: "Wert muss mindestens {{0}} sein",
  error_maxLength: "Wert darf höchstens {{0}} Zeichen lang sein",
  // error_contains: "No items match contains",
  error_minContains:
    "Contains match count {{0}} is less than minimum contains count of {{1}}",
  error_maxContains:
    "Contains match count {{0}} exceeds maximum contains count of {{1}}",
  error_minLength: "Value must be at least {{0}} characters long",
  error_pattern: "Value must match the pattern {{0}}",
  error_additionalItems: "No additional items allowed in this array",
  error_maxItems: "Value must have at most {{0}} items",
  error_minItems: "Value must have at least {{0}} items",
  error_uniqueItems: "Array must have unique items",
  error_maxProperties: "Object must have at most {{0}} properties",
  error_minProperties: "Object must have at least {{0}} properties",
  error_required: "Object is missing the required property '{{0}}'",
  error_additional_properties:
    "No additional properties allowed, but property {{0}} is set",
  error_property_names_exceeds_maxlength:
    "Property name {{0}} exceeds maxLength",
  error_property_names_enum_mismatch:
    "Property name {{0}} does not match any enum values",
  error_property_names_const_mismatch:
    "Property name {{0}} does not match the const value",
  error_property_names_pattern_mismatch:
    "Property name {{0}} does not match pattern",
  error_property_names_false:
    "Property name {{0}} fails when propertyName is false",
  error_property_names_maxlength:
    "Property name {{0}} cannot match invalid maxLength",
  error_property_names_enum: "Property name {{0}} cannot match invalid enum",
  error_property_names_pattern:
    "Property name {{0}} cannot match invalid pattern",
  error_property_names_unsupported: "Unsupported propertyName {{0}}",
  error_dependency: "Must have property {{0}}",
  error_date: "Date must be in the format {{0}}",
  error_time: "Time must be in the format {{0}}",
  error_datetime_local: "Datetime must be in the format {{0}}",
  error_invalid_epoch: "Date must be greater than 1 January 1970",
  error_ipv4:
    "Value must be a valid IPv4 address in the form of 4 numbers between 0 and 255, separated by dots",
  error_ipv6: "Value must be a valid IPv6 address",
  error_hostname: "The hostname has the wrong format",
  upload_max_size: "Datei zu gross. Maximale Grösse ist ",
  upload_wrong_file_format: "Falsches Dateiformat. Erlaubte Formate: ",
  button_save: "Sichern",
  button_copy: "Kopieren",
  button_cancel: "Abbrechen",
  button_add: "Hinzufügen",
  button_delete_all: "Alle",
  button_delete_all_title: "Alle löschen",
  button_delete_last: "Letztes {{0}}",
  button_delete_last_title: "Letztes {{0}} löschen",
  button_add_row_title: "{{0}} hinzufügen",
  button_move_down_title: "Nach hinten",
  button_move_up_title: "Nach vorne",
  button_properties: "Eigenschaften",
  button_object_properties: "Objekteigenschaften",
  button_copy_row_title: "{{0}} kopieren",
  button_delete_row_title: "{{0}} löschen",
  button_delete_row_title_short: "Löschen",
  button_copy_row_title_short: "Kopieren",
  button_collapse: "Einklappen",
  button_expand: "Aufklappen",
  button_edit_json: "JSON bearbeiten",
  button_upload: "Hochladen",
  flatpickr_toggle_button: "Umschalten",
  flatpickr_clear_button: "Leeren",
  choices_placeholder_text: "Tippen um einen Wert hinzuzufügen",
  default_array_item_title: "Element",
  button_delete_node_warning: "Dieses Element wirklich löschen?",
}
