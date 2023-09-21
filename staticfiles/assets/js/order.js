var mix = {
	data() {
		return {
			payload: {
				full_name: '',
				phone: '',
				email: '',
				address: '',
				delivery_id: null,
			},
			carts: [],
			deliveries: [],
		};
	},
	async mounted() {
		this.payload.full_name = userFullName;
		this.payload.phone = userPhone;
		this.payload.email = userEmail;
		this.payload.address = userAddress;
		this.carts = await this.getUserCarts();
		this.deliveries = await this.getDeliveries();
		const deliveriesIDs = this.deliveries.map((d) => d.id);
		const deliveriesIDsLen = deliveriesIDs.length;
		this.payload.delivery_id = deliveriesIDsLen > 0 ? deliveriesIDs[deliveriesIDsLen - 1] : null;
	},
	methods: {
		async createOrder() {
			axios.defaults.xsrfCookieName = 'csrftoken';
			axios.defaults.xsrfHeaderName = 'X-CSRFToken';
			await axios.post('http://0.0.0.0:8000/api/order', this.payload, {
				headers: {
					Accept: 'application/json',
					'Content-Type': 'application/json',
					'X-Sessionid': this.getCookie('sessionid'),
				},
				withCredentials: true,
			});
		},
		async getDeliveries() {
			resp = await axios.get('http://0.0.0.0:8000/api/delivery');
			return resp.data;
		},
	},
};
