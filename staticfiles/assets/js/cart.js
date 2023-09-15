var mix = {
	data() {
		return {
			carts: [],
			cartsList: [],
		};
	},
	async mounted() {
		this.carts = await this.getUserCarts();
		this.cartsList = this.carts.map((p) => p.products_count);
	},
	methods: {
		async getUserCarts() {
			axios.defaults.xsrfCookieName = 'csrftoken';
			axios.defaults.xsrfHeaderName = 'X-CSRFToken';
			let resp = await axios.get('http://0.0.0.0:8000/api/cart', {
				headers: {
					Accept: 'application/json',
					'Content-Type': 'application/json',
					'X-Sessionid': this.getCookie('sessionid'),
				},
				withCredentials: true,
			});
			return resp.data;
		},
		async deleteCartByID(cartID) {
			axios.defaults.xsrfCookieName = 'csrftoken';
			axios.defaults.xsrfHeaderName = 'X-CSRFToken';
			await axios
				.delete(`http://0.0.0.0:8000/api/cart/${cartID}`, {
					headers: {
						Accept: 'application/json',
						'Content-Type': 'application/json',
						'X-Sessionid': this.getCookie('sessionid'),
					},
					withCredentials: true,
				})
				.then(async () => {
					this.carts = await this.getUserCarts();
				});
		},
		async updateCartByID(cartID, payload) {
			axios.defaults.xsrfCookieName = 'csrftoken';
			axios.defaults.xsrfHeaderName = 'X-CSRFToken';
			resp = await axios.put(`http://0.0.0.0:8000/api/cart/${cartID}`, payload, {
				headers: {
					Accept: 'application/json',
					'Content-Type': 'application/json',
					'X-Sessionid': this.getCookie('sessionid'),
				},
				withCredentials: true,
			});
			return resp.data;
		},
		async updateCartCount(index) {
			try {
				let cart = await this.updateCartByID(this.carts[index].id, { products_count: this.carts[index].products_count });
				this.carts[index].products_count = cart.products_count;
				this.cartsList[index] = cart.products_count;
			} catch (err) {
				this.carts[index].products_count = this.cartsList[index];
			}
		},
		async incrementCartCount(index) {
			try {
				this.carts[index].products_count = Number(this.carts[index].products_count) + 1;
			} catch (err) {}
			await this.updateCartCount(index);
		},
		async decrementCartCount(index) {
			try {
				this.carts[index].products_count = Number(this.carts[index].products_count) - 1;
			} catch (err) {}
			await this.updateCartCount(index);
		},
	},
};
