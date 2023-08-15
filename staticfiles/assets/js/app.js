const { createApp } = Vue;
createApp({
	delimiters: ['${', '}$'],
	mixins: [window.mix ? window.mix : {}],
}).mount('#app');
