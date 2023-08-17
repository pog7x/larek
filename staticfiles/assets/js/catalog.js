var mix = {
	data() {
		return {
			query: {
				price__gte: '1',
				price__lte: '50000',
				product__name__icontains: '',
				in_stock: '',
				ordering: '-product__views_history__count',
				page: 1,
			},
			max_count: 1,
			product_sellers: null,
			loading: false,
			errored: false,
			order_by: [
				{ id: 'product__views_history__count', title: 'Популярности' },
				{ id: 'product__review__count', title: 'Отзывам' },
				{ id: 'product__id', title: 'Новизне' },
				{ id: 'price', title: 'Цене' },
			],
			order_dir: '-',
			order_dir_map: {
				'': 'dec',
				'-': 'inc',
			},
		};
	},
	mounted() {
		const urlSearchParams = new URLSearchParams(window.location.search);
		const params = Object.fromEntries(urlSearchParams.entries());
		this.query = { ...this.query, ...params };
		this.order_dir = this.query.ordering.startsWith('-') ? '-' : '';
		this.changePage(this.query.page);
		this.updateSearch();
		this.fetchProductSeller();
	},
	methods: {
		filterForm() {
			this.query.price__gte = document.querySelector('input[name=price__gte]').value;
			this.query.price__lte = document.querySelector('input[name=price__lte]').value;
			this.updateSearch();
			this.fetchProductSeller();
		},
		fetchProductSeller() {
			axios
				.get('http://0.0.0.0:8000/api/product_seller', {
					params: { ...this.query },
				})
				.then((response) => {
					this.product_sellers = response.data.results;
					this.max_count = response.data.count;
				})
				.catch((error) => {
					console.log(error);
					this.errored = true;
				})
				.finally(() => (this.loading = false));
		},
		setSort(id) {
			this.order_dir = this.order_dir === '-' && this.query.ordering.endsWith(id) ? '' : '-';
			this.query.ordering = `${this.order_dir}${id}`;
			this.updateSearch();
			this.fetchProductSeller();
		},
		updateSearch() {
			const new_search = new URLSearchParams([...Object.entries(this.query)]).toString();
			window.history.replaceState(null, null, `?${new_search}`);
		},
		changePage(param) {
			const new_page = Number(param);
			const max_pages = Math.ceil(Number(this.max_count) / 9);
			console.log(new_page, max_pages);
			if (new_page <= 0 || new_page > max_pages) {
				this.query.page = 1;
			} else {
				this.query.page = new_page;
			}
			this.fetchProductSeller();
			this.updateSearch();
		},
	},
};
