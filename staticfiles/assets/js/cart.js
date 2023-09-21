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
					this.cartsList = this.carts.map((p) => p.products_count);
					this.cartTotalData = await this.getCartTotal();
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
		async updateCartCount(index, newRes = null) {
			try {
				let cart = await this.updateCartByID(this.carts[index].id, { products_count: newRes });
				this.carts[index].products_count = cart.products_count;
			} catch (err) {
			} finally {
				this.cartTotalData = await this.getCartTotal();
				this.cartsList[index] = this.carts[index].products_count;
			}
		},
		async incrementCartCount(index) {
			try {
				let newRes = Number(this.cartsList[index]) + 1;
				await this.updateCartCount(index, newRes);
			} catch (err) {
				this.cartsList[index] = this.carts[index].products_count;
			}
		},
		async decrementCartCount(index) {
			try {
				let newRes = Number(this.cartsList[index]) - 1;
				await this.updateCartCount(index, newRes);
			} catch (err) {
				this.cartsList[index] = this.carts[index].products_count;
			}
		},
	},
};
