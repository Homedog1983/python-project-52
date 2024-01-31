class AddCreatorMixin:
    """
    Add authenticated user as task.creator
    for creation.
    ! Use after is_authenticated = True check !
    """
    def form_valid(self, form):
        if self.request.method == 'POST':
            task = form.save(commit=False)
            task.creator = self.request.user
        return super().form_valid(form)
