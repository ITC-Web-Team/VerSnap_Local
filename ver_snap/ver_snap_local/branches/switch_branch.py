from models.models import Branch , ActiveBranch
from django.db import transaction

def switch_branch(branch_name):
    """
    Switch to the specified branch in the version control system.

    Args:
        branch_name (str): Name of the branch to switch to.

    Returns:
        str: A message indicating the success or failure of the operation.
    """
    try:
        # Check if the branch exists
        branch = Branch.objects.get(name=branch_name)
    except Branch.DoesNotExist:
        return f"Error: Branch '{branch_name}' does not exist!"

    try:
        # Check if there's already an active branch
        active_branch = ActiveBranch.objects.get(id=1)  # Assuming a single active branch exists
    except ActiveBranch.DoesNotExist:
        active_branch = None

    if active_branch is not None and active_branch.branch.name == branch_name:
        return f"Warning: Already on the branch: {branch_name}"

    with transaction.atomic():
        if active_branch is None:
            # If no active branch exists, set the new branch as active
            ActiveBranch.objects.create(branch=branch)
        else:
            # Switch to the new branch
            old_active_branch = active_branch.branch
            active_branch.branch = branch
            active_branch.save()
            return f"Successfully switched from branch {old_active_branch.name} to {branch_name}"

    # Confirm the current active branch
    active_branch = ActiveBranch.objects.get(id=1)
    return f"Successfully switched to the branch: {branch_name}\nCurrent active branch: {active_branch.branch.name}"

