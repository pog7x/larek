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
			await this.axios.delete(`/api/cart/${cartID}`).then(async () => {
				this.carts = await this.getUserCarts();
				this.cartsList = this.carts.map((p) => p.products_count);
				this.cartTotalData = await this.getCartTotal();
			});
		},
		async updateCartCount(index, newRes = null) {
			try {
				let cart = await this.updateCartByID(this.carts[index].id, { products_count: newRes });
				if (this.carts[index].products_count === cart.products_count) {
					return;
				}
				this.carts[index].products_count = cart.products_count;
			} catch (err) {}
			this.cartTotalData = await this.getCartTotal();
			this.cartsList[index] = this.carts[index].products_count;
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
