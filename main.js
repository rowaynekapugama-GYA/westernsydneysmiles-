
(function(){
  // reveal on scroll
  var els=document.querySelectorAll('.offer-card,.feat,.tm,.proc > div,.urgent-list > div,.row');
  els.forEach(function(e){e.classList.add('reveal')});
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{rootMargin:'0px 0px -8% 0px'});
    els.forEach(function(e){io.observe(e)});
  }else{els.forEach(function(e){e.classList.add('in')})}

  // smooth anchor + focus first field when jumping to form
  document.querySelectorAll('a[href="#book"]').forEach(function(a){
    a.addEventListener('click',function(ev){
      var t=document.getElementById('book'); if(!t) return;
      ev.preventDefault(); t.scrollIntoView({behavior:'smooth',block:'start'});
      setTimeout(function(){var f=document.getElementById('fname'); if(f && window.innerWidth>960) f.focus({preventScroll:true})},600);
      window.dataLayer=window.dataLayer||[]; window.dataLayer.push({event:'book_click'});
    });
  });
  document.querySelectorAll('.js-call').forEach(function(a){a.addEventListener('click',function(){window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:'call_click'})})});
  document.querySelectorAll('.js-sched-open').forEach(function(a){a.addEventListener('click',function(){window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:'scheduler_open'})})});

  // scheduler engagement: fires once when the visitor clicks into the embedded booking frame
  var fr=document.querySelector('.sched-frame iframe');
  if(fr){var fired=false; window.addEventListener('blur',function(){ if(!fired && document.activeElement===fr){fired=true; window.dataLayer=window.dataLayer||[]; window.dataLayer.push({event:'scheduler_engaged'});} });}
  // open the call-back form if linked to directly
  if(location.hash==='#callback'){var cb=document.getElementById('callback'); if(cb) cb.open=true;}

  // booking form
  var form=document.getElementById('bookingForm'); if(!form) return;
  var msg=document.getElementById('formMsg'), btn=document.getElementById('submitBtn');
  function bad(el){el.style.borderColor='#E24B4B'; el.addEventListener('input',function(){el.style.borderColor=''},{once:true})}
  form.addEventListener('submit',function(ev){
    ev.preventDefault(); msg.className='form-msg'; msg.textContent='';
    if(form.website.value){return}  // honeypot
    var ok=true;
    ['first_name','last_name','mobile','email'].forEach(function(n){var el=form[n]; if(!el.value.trim()){bad(el);ok=false}});
    var m=form.mobile.value.replace(/\s+/g,''); if(m && !/^(\+?61|0)[2-9]\d{8}$/.test(m)){bad(form.mobile);ok=false}
    if(form.email.value && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(form.email.value)){bad(form.email);ok=false}
    if(!ok){msg.className='form-msg err';msg.textContent='Please check the highlighted fields and try again.';return}
    btn.disabled=true; btn.innerHTML='Sending your request…';
    var data={}; new FormData(form).forEach(function(v,k){data[k]=v}); data.page_url=location.href; data.submitted_at=new Date().toISOString();
    var endpoint=form.getAttribute('action');
    var done=function(){
      window.dataLayer=window.dataLayer||[]; window.dataLayer.push({event:'booking_request',service:data.service,patient_type:data.patient_type});
      try{sessionStorage.setItem('wss_lead',JSON.stringify({first_name:data.first_name,service:data.service,preferred_day:data.preferred_day,preferred_time:data.preferred_time}))}catch(e){}
      location.href='thank-you.html';
    };
    if(!endpoint || endpoint==='#'){setTimeout(done,700);return}
    fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(function(r){if(!r.ok)throw 0;done()}).catch(function(){
      btn.disabled=false; btn.innerHTML='Try again';
      msg.className='form-msg err'; msg.innerHTML='Something went wrong sending your request. Please call us on <a href="tel:0296237333" style="color:inherit;text-decoration:underline">(02) 9623 7333</a>.';
    });
  });
})();
