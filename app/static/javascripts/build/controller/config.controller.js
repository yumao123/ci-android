/*
	打包配置页面控制器
*/
angular
	.module("buiploy.building")
	.controller("BuildConfigController", BuildConfigController);

BuildConfigController.$inject = ["$scope", "$rootScope", "$interval", "BussinessService", "$modal", "$log", ]

function BuildConfigController($scope, $rootScope, $interval, BussinessService, $modal, $log){

	/*
		页码初始化
	*/
	$scope.paginationConf = {
		currentPage: 1,
		itemsPerPage: 10,
	};

	/*
		新增开关配置文件
	*/
	$scope.add_file = function(){
		var modalInstance = $modal.open({
			templateUrl : "/api/template/modal_config_add",
			controller: "AddConfigModalInstanceCtrl",
			size: 'lg',
			backdrop: 'static',
			resolve: {
				modal_info: function(){
					return {
						modal_name: '新增配置文件',
						GetTableRows: GetTableRows,
					};
				},
			},
		})
		modalInstance.result.then(
			function(result){
				GetTableRows();
			},
			function(){
				/*do nothing*/
			}
		);
	};

	/*
		查看配置文件-开关详情
	*/
	var showDetail = function($index){
		var modalInstance = $modal.open({
			templateUrl : "/api/template/modal_config",
			controller: "ConfigModalInstanceCtrl",
			size: 'lg',
			backdrop: 'static',
			resolve: {
				modal_info: function(){
					return {
						file_nick_name: $scope.config_list[$index].file_nick_name,
						GetTableRows: GetTableRows,
						modal_name: '开关详情设置'
					};
				},
			},
		})
	};

	/*
		初始化表格label
	*/
	var GetTableColumns = function(){
		var postData = {
			item_name : "buildConfigModule"
		};

		var postUrl = "/api/get_tableTitle";

		BussinessService.list(postData, postUrl).success(function(response){
			$scope.tableConf.colums = response.columns

			/*
				监听页码变动，获取表格数据
			*/
			$scope.$watch('paginationConf.currentPage + paginationConf.itemsPerPage', GetTableRows);
		});
	};

	/*
		获取表格数据
	*/
	var GetTableRows = function(){
		var postData = {
			item_name : "buildConfigModule",
			pageIndex: $scope.paginationConf.currentPage,
			pageSize: $scope.paginationConf.itemsPerPage
		};

		var postUrl = "/api/get_tableInfo";

		BussinessService.list(postData, postUrl).success(function (response) {
			$scope.paginationConf.totalItems = response.count;
			$scope.config_list = response.data_list;

			//package rows -> cells
			$scope.tableConf.rows = []
			for (var i= 0; i < $scope.config_list.length; i++){
				$scope.tableConf.rows.push({cells: []});
				for (var x=0; x < $scope.tableConf.colums.length; x++){
					var key = $scope.tableConf.colums[x].name
					$scope.tableConf.rows[i].cells.push($scope.config_list[i][key])
				}
			}
		});
	}	

	/*
		初始化表格信息
	*/
	$scope.tableConf = {
		id: "android_table",
		checked: false,
		class: "table table-bordered table-hover",
		getColumns: GetTableColumns,
		clickFunc: showDetail,
	}


}


angular
	.module("buiploy.building")
	.controller("ConfigModalInstanceCtrl", ConfigModalInstanceCtrl);

ConfigModalInstanceCtrl.$inject = ["$scope", "$modalInstance", "modal_info", "BussinessService", "$rootScope"]

/*
	新增、设置控件开关静态框
*/
function ConfigModalInstanceCtrl($scope, $modalInstance, modal_info, BussinessService, $rootScope){
	$scope.modal_info = modal_info
	$scope.current_config = {}


	var showDetail = function(){
		var postData = {
			file_nick_name: $scope.modal_info.file_nick_name
		}

		var postUrl = "/api/get_current_switch"

		BussinessService.list(postData, postUrl).success(function(response){
			$scope.current_switch = response.configInfo
		});
	};


	$scope.add_items = function(){
		var items = {
			item_name: '',
			item_type: 'text',
			isshow: 'true',
			description: '',
		};
		$scope.current_switch.file_items.push(items)
	}

	$scope.minus_items = function($index){
		$scope.current_switch.file_items.splice($index, 1)
	};

	$scope.ok = function(){
		//package value
		var ret = {}
		var postData = {
			modify_switch: $scope.current_switch.file_items,
			file_nick_name: $scope.current_switch.file_nick_name,
		}

		var postUrl = "/api/modify_switch"
		BussinessService.list(postData, postUrl)
			.success(function(response){
				swal({
					title: $scope.modal_info.modal_name, text: response.result, type: "success", timer: 1500,
					showConfirmButton: false,
				});
			})
			.error(function(response){
				swal({
					title: $scope.modal_info.modal_name, text: response.result, type: "error", timer: 1500,
					showConfirmButton: false,
				});
			})
		$modalInstance.close();	
	};

	$scope.cancel = function(){
		$modalInstance.dismiss('cancel');
	}

	$scope.delete = function(){
		var postData = {
			file_nick_name: $scope.current_switch.file_nick_name
		}

		var postUrl = "/api/delete_config_file"
		BussinessService.list(postData, postUrl)
			.success(function(response){
				swal({
					title: $scope.modal_info.modal_name, text: response.result, type: "success", timer: 1500,
					showConfirmButton: false,
				});
				modal_info.GetTableRows();
			})
			.error(function(response){
				swal({
					title: $scope.modal_info.modal_name, text: response.result, type: "error", timer: 1500,
					showConfirmButton: false,
				});
			})
		$modalInstance.close();	
	};

	showDetail();

}

angular
	.module("buiploy.building")
	.controller("AddConfigModalInstanceCtrl", AddConfigModalInstanceCtrl);

AddConfigModalInstanceCtrl.$inject = ["$scope", "$modalInstance", "modal_info", "BussinessService"]

/*
	新增配置文件静态框
*/
function AddConfigModalInstanceCtrl($scope, $modalInstance, modal_info, BussinessService){
	$scope.modal_info = modal_info;

	/*
		新增配置文件
	*/
	$scope.ok = function(){
		//package value
		var postData = {
			add_config_file: $scope.formData
		}

		var postUrl = "/api/add_config_file"

		BussinessService.list(postData, postUrl).success(function(response){
				swal({
					title: $scope.modal_info.modal_name, text: response.result, type: "success", timer: 1500,
					showConfirmButton: false,
				});
				modal_info.GetTableRows();
			})
			.error(function(response){
				swal({
					title: $scope.modal_info.modal_name, text: response.result, type: "error", timer: 1500,
					showConfirmButton: false,
				});
			})

		$modalInstance.close();
	};

	$scope.cancel = function(){
		$modalInstance.dismiss('cancel');
	}

}
