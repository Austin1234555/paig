import React, { Component } from "react";

import VEvaluationCategoriesForm from "components/audits/evaluation/v_evaluation_categories_form";

class CEvaluationCategoriesForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      showSuggested: true,
      selectedCategories: []
    };
  }

  componentDidMount() {
    const { _vState } = this.props;
    const evalCategories = _vState.purposeResponse;
    const hasSuggestedCategories = evalCategories?.suggested_categories?.length > 0;
    
    if (hasSuggestedCategories) {
      // If there are suggested categories, use them and select them by default
      const categories = evalCategories.suggested_categories.map((category) => category.Name);
      this.props.form.refresh({ categories });
      this.setState({ selectedCategories: categories });
    } else {
      // If there are no suggested categories, don't select any by default
      this.setState({ 
        showSuggested: false,
        selectedCategories: [] 
      });
      this.props.form.refresh({ categories: [] });
    }
  }

  handleToggle = () => {
    const { _vState } = this.props;
    const evalCategories = _vState.purposeResponse;
    
    this.setState((prevState) => {
      const showSuggested = !prevState.showSuggested;
      // Keep the existing selections when toggling
      return {
        showSuggested
      };
    });
  };

  setSelectedCategories = (selectedCategories) => {
    this.setState({ selectedCategories });
    this.props.form.refresh({ categories: selectedCategories });
  };

  render() {
    const { selectedCategories, showSuggested } = this.state;
    const { _vState } = this.props;
    const evalCategories = _vState.purposeResponse;
    // Only filter what categories to show, but maintain selections
    const filteredCategories = showSuggested && evalCategories?.suggested_categories?.length > 0 ? 
      evalCategories.suggested_categories : 
      evalCategories.all_categories;

    return (
      <VEvaluationCategoriesForm
        form={this.props.form}
        selectedCategories={selectedCategories}
        showSuggested={showSuggested}
        handleToggle={this.handleToggle}
        filteredCategories={filteredCategories}
        setSelectedCategories={this.setSelectedCategories}
        _vState={_vState}
      />
    );
  }
}

export default CEvaluationCategoriesForm;