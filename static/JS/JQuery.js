$(function() {
    $("#date").datepicker({
      dateFormat: "yy/mm/dd",
      minDate: new Date(2023, 3, 1) // 4月1日以降に制限
    });
  });